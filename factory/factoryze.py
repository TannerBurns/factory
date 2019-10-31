import os
import sys
import json
import time
import asyncio
import hashlib
import concurrent.futures

from math import ceil
from functools import partial
from uuid import uuid4
from typing import Callable, Iterable, Tuple
from multiprocessing import Pool

from .models import Task, Operation, Runtime, Content, Session

from vast import Vast

class Factoryze(object):
    """factoryze -- class for running user functions and saving results"""
    def __init__(self, operators=4, workers=16, session=f'factoryze-session-{str(time.time())}'):
        self.operators = operators
        self.workers = workers
        self.session = session.replace(".", "-")

    def factoryze(self, fn: Callable, args: list= [], kwargs: dict= {}) -> str:
        """factoryze
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
            if args and not kwargs:
                ret = fn(*args)
            elif kwargs and not args:
                ret = fn(**kwargs)
            elif args and kwargs:
                ret = fn(*args, **kwargs)
            else:
                ret = fn()
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

        