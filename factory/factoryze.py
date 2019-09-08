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

from .models import Task, Operation, Runtime, Content

class factoryze:
    def __init__(self, operators=4, workers=16, session=str(uuid4())):
        self.operators = operators
        self.workers = workers
        self.session = session

    def start(self, fn: Callable, args: list) -> str:
        task_id = str(uuid4())
        start = time.time()
        status = "IN PROGRESS"

        operation, created = Operation.objects.get_or_create(
            name = self.operation.get("name"), 
            docstring = self.operation.get("doc"),
            hash = self.operation.get("hash"),
            sha256 = self.operation.get("sha256")
        )
        operation.save()
        
        task = Task.objects.create(
            task = task_id,
            session = self.session,
            status = status,
            operation = operation
        )
        task.save()

        runtime = Runtime.objects.create(start=time.time(), task=task)
        runtime.save()

        
        
        try:
            ret = fn(args)
            status = "COMPLETE"
            if ret:
                results = json.dumps(ret)
                errors = json.dumps([])
            if not ret:
                errors = json.dumps(["no results or errors found, reporting as failed"])
                status = "FAILED"
        except Exception as err:
            status = "ERROR"
            errors = json.dumps([str(err)])
            results = json.dumps([])            
        
        content = Content.objects.create(results=results, errors=errors, task=task)
        content.save()

        task.status = status
        task.save()
      
        runtime.stop = time.time()
        runtime.total = runtime.stop - start
        runtime.save()


        return task_id

    
    async def _worker(self, fn:Callable, group: list) -> list:
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.workers) as executor:
            #self.loop = asyncio.get_event_loop()
            futures = [
                self.loop.run_in_executor(executor, partial(fn, item)) 
                for item in group if item
            ]
        await asyncio.gather(*futures)
        return [f.result() for f in futures]
    
    def _factoryze_operator(self, fn: Callable, args: list) -> list:
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
        self.operation = {
            "name": fn.__name__,
            "doc": fn.__doc__ if fn.__doc__ else "None",
            "hash": fn.__hash__(),
            "sha256": hashlib.sha256(
                fn.__name__.encode()+fn.__doc__.encode()+str(fn.__hash__()).encode()
            ).hexdigest()
        }

        csize = int(len(args)/self.operators) if int(len(args)/self.operators) > 0 else 1
        chunked = [
            args[ind:ind+int(len(args)/self.operators)]
            for ind in range(0, len(args), csize)
        ]
        operator = partial(self._factoryze_operator, fn)
        manager = partial(self.start, operator)
        with Pool(processes=self.operators) as pool:
            return pool.map(manager, chunked)
    
    def multiprocess_factoryze(self, fn: Callable, args: list) -> list:
        self.operation = {
            "name": fn.__name__,
            "doc": fn.__doc__ if fn.__doc__ else "None",
            "hash": fn.__hash__(),
            "sha256": hashlib.sha256(
                bytesarray(fn.__name__)+bytesarray(fn.__doc__)+bytesarray(fn.__hash__())
            ).hexdigest()
        }

        chunked = [
            args[ind:ind+self.workers]
            for ind in range(0, len(args), self.workers)
        ]
        with Pool(processes=self.operators) as pool:
            return [
                res
                for ind in range(0, len(chunked), self.operators)
                for res in pool.map(partial(self.start, fn), chunked[ind:ind+self.operators])
                if res
            ]
    
    def async_factoryze(self, fn: Callable, args: list) -> list:
        self.operation = {
            "name": fn.__name__,
            "doc": fn.__doc__ if fn.__doc__ else "None",
            "hash": fn.__hash__(),
            "sha256": hashlib.sha256(
                bytesarray(fn.__name__)+bytesarray(fn.__doc__)+bytesarray(fn.__hash__())
            ).hexdigest()
        }

        operator = partial(self._factoryze_operator, fn)
        manager = partial(self.start, operator)
        for ind in range(0, len(args), self.workers):
            yield manager(args[ind:ind+self.workers])