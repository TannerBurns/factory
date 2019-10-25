import os
import sys
import json
import time
import asyncio
import hashlib
import concurrent.futures

from functools import partial
from uuid import uuid4
from typing import Callable, Iterable, Tuple
from multiprocessing import Pool

from .models import Task, Operation, Runtime, Content, Session

class factoryze:
    """factoryze -- class for running user functions and saving results"""
    def __init__(self, operators=4, workers=16, session=f'factoryze-client-{str(time.time())}'):
        self.operators = operators
        self.workers = workers
        self.session = session.replace(".", "-")

    def start(self, fn: Callable, args: list) -> str:
        """start -- function for running function and saving results into models
        
        Arguments:
            fn {Callable} -- user defined function for factory
            args {list} -- list of arguments for the user defined function
        
        Returns:
            str -- task id
        """

        # initialize vars
        task_id = str(uuid4())
        start = time.time()
        status = "IN PROGRESS"

        # find current session objects with same name
        session = Session.objects.all().filter(name=self.session)
        if len(session) > 0: # get first item from QuerySet
            session = session[0]
        else: # create new session object
            session, _ = Session.objects.get_or_create(name=self.session)

        if not hasattr(self, 'operation'):
            name = fn.__name__ if fn.__name__ else ""
            doc = fn.__doc__ if fn.__doc__ else ""
            self.operation = {
                "name": name,
                "doc": doc,
                "hash": fn.__hash__(),
                "sha256": hashlib.sha256(
                    name.encode()+doc.encode()+str(fn.__hash__()).encode()
                ).hexdigest()
            }

        # get or create operation object if it does not exist
        operation, _ = Operation.objects.get_or_create(
            name = self.operation.get("name"), 
            docstring = self.operation.get("doc"),
            hash = self.operation.get("hash"),
            sha256 = self.operation.get("sha256")
        )
        operation.save()

        # create a new task object as if every task is a new one
        task = Task.objects.create(
            task = task_id,
            status = status,
            operation = operation
        )
        task.save()

        # add task to the current session
        session.tasks.add(task)
        session.save()

        # create a new runtime object
        runtime = Runtime.objects.create(start=time.time(), task=task)
        runtime.save()
        
        results = []
        errors = []
        # get results from given function with given args
        try:
            # call function with arguments
            ret = fn(args)
            # set status to complete after function finishes
            status = "COMPLETE"

            # check if there was any results
            if ret:
                # set results and errors (no errors found yet)
                results = ret
                errors = []
                # check if user function returns as results and errors in a dict (will flatten results)
                if type(ret) == dict:
                    # check for keys and save if found
                    if "results" in ret and "errors" in ret:
                        results = ret.get("results")
                        errors = ret.get("errors")
            else:
                # no results were found but no errors, function was probably not returning anything
                errors = ["no results or errors found, reporting as failed"]
                # set status to failed since task performed blank work
                status = "FAILED"   
        except Exception as err:
            # something went wrong in the function that threw an exception, status set to error
            status = "ERROR"
            # add error string to errors
            errors = [str(err)]
            results = []

        # attempt to create new content only if results have not been seen before
        try:
            # check if input and output already exist
            content = Content.objects.get(
                input_type = str(type(args[0])),
                input_count = len(args),
                input_sha256 = hashlib.sha256(
                    str(args).encode()
                ).hexdigest(),
                output_count = len(results),
                output_sha256 = hashlib.sha256(
                    str(str(results)+str(errors)).encode()
                ).hexdigest(),
                errors = json.dumps(errors),
                results = json.dumps(results)
            )

            # if duplicate work, clean up temporary model objects
            session.tasks.remove(task)
            session.save()
            task.delete()
            runtime.delete()

            # add session to task if new
            task = Task.objects.get(task=content.task.task)
            tids = set([t.id for t in session.tasks.all()])
            if task.id not in tids:
                session.tasks.add(task)
                session.save()
            
            # return already worked task id
            return content.task.task
        except Content.DoesNotExist:
            # handle new content
            content = Content.objects.create(
                input_type = str(type(args[0])),
                input_count = len(args),
                input_sha256 = hashlib.sha256(
                    str(args).encode()
                ).hexdigest(),
                output_count = len(results),
                output_sha256 = hashlib.sha256(
                    str(str(results)+str(errors)).encode()
                ).hexdigest(),
                errors = json.dumps(errors),
                results = json.dumps(results),
                task = task
            )
            content.save()

        # set the task status
        task.status = status
        task.save()
    
        # set the runtime for task
        runtime.stop = time.time()
        runtime.total = runtime.stop - start
        runtime.save()

        # return task id
        return task.task

    
    async def _worker(self, fn:Callable, group: list) -> list:
        """_worker -- does the job and returns the results
        
        Arguments:
            fn {Callable} -- user defined function for factory
            args {list} -- list of arguments for the user defined function
        
        Returns:
            list -- list of returned values from the user defined function
        """
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.workers) as executor:
            futures = [
                self.loop.run_in_executor(executor, partial(fn, item)) 
                for item in group if item
            ]
        await asyncio.gather(*futures)
        return [f.result() for f in futures]
    

    def _operator(self, fn: Callable, args: list) -> list:
        """_operator -- controls all the current workers and combines their returns
        
        Arguments:
            fn {Callable} -- user defined function for factory
            args {list} -- list of arguments for the user defined function
        
        Returns:
            list -- list of returned values from the user defined function
        """

        self.loop = asyncio.new_event_loop()
        return [
            res
            for ind in range(0, len(args), self.workers)
            for res in self.loop.run_until_complete(
                self._worker(fn, args[ind:ind+self.workers])
            )
            if res
        ]
    

    def factoryze(self, fn: Callable, args: list) -> list:
        """factoryze -- run jobs using multiproccess and asnyc functionality
        
        Arguments:
            fn {Callable} -- user defined function for factory
            args {list} -- list of arguments for the user defined function
        
        Returns:
            list -- list of returned values from the user defined function
        """

        # get vars related to function definition
        name = fn.__name__ if fn.__name__ else ""
        doc = fn.__doc__ if fn.__doc__ else ""

        # set current operation for class
        self.operation = {
            "name": name,
            "doc": doc,
            "hash": fn.__hash__(),
            "sha256": hashlib.sha256(
                name.encode() + doc.encode() + str(fn.__hash__()).encode()
            ).hexdigest() # create sha256 hash for operation
        }

        # get chunk size to evenly distribute work
        size = int(len(args)/self.operators)
        csize =  size if size > 0 else 1

        # create chunks based off chunk size
        chunked = [
            args[ind:ind+int(len(args)/self.operators)]
            for ind in range(0, len(args), csize)
        ]

        # initialize the operator function
        operator = partial(self._operator, fn)
        # create a manager function to start the operator and workers
        manager = partial(self.start, operator)
        # start the process pools
        with Pool(processes=self.operators) as pool:
            return pool.map(manager, chunked)
    

    def multiprocess_factoryze(self, fn: Callable, args: list) -> list:
        """multiprocess_factoryze -- run jobs using only multiproccess functionality
        
        Arguments:
            fn {Callable} -- user defined function for factory
            args {list} -- list of arguments for the user defined function
        
        Returns:
            list -- list of returned values from the user defined function
        """

        # get vars related to function definition
        name = fn.__name__ if fn.__name__ else ""
        doc = fn.__doc__ if fn.__doc__ else ""

        # set current operation for class
        self.operation = {
            "name": name,
            "doc": doc,
            "hash": fn.__hash__(),
            "sha256": hashlib.sha256(
                name.encode()+doc.encode()+str(fn.__hash__()).encode()
            ).hexdigest()
        }

        # create chunks based off workers size
        chunked = [
            args[ind:ind+self.workers]
            for ind in range(0, len(args), self.workers)
        ]

        # iterate over chunks of process pools and combine the results
        with Pool(processes=self.operators) as pool:
            return [
                res
                for ind in range(0, len(chunked), self.operators)
                for res in pool.map(partial(self.start, fn), chunked[ind:ind+self.operators])
                if res
            ]
    

    def async_factoryze(self, fn: Callable, args: list) -> list:
        """async_factoryze -- run jobs using only asnyc functionality
        
        Arguments:
            fn {Callable} -- user defined function for factory
            args {list} -- list of arguments for the user defined function
        
        Returns:
            list -- list of returned values from the user defined function
        """

        # get vars related to function definition
        name = fn.__name__ if fn.__name__ else ""
        doc = fn.__doc__ if fn.__doc__ else ""

        # set current operation for class
        self.operation = {
            "name": name,
            "doc": doc,
            "hash": fn.__hash__(),
            "sha256": hashlib.sha256(
                name.encode()+doc.encode()+str(fn.__hash__()).encode()
            ).hexdigest()
        }

        # initialize the operator function
        operator = partial(self._operator, fn)
        # create a manager function to start the operator and workers
        manager = partial(self.start, operator)
        # loop through and yeild the manager's returned work
        for ind in range(0, len(args), self.workers):
            yield manager(args[ind:ind+self.workers])