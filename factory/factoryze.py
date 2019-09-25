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
        
        try:
            ret = fn(args)
            status = "COMPLETE"
            if ret:
                results = ret
                errors = []
                if type(ret) == dict:
                    if "results" in ret and "errors" in ret:
                        results = ret.get("results")
                        errors = ret.get("errors")
            if not ret:
                errors = ["no results or errors found, reporting as failed"]
                status = "FAILED"
        except Exception as err:
            status = "ERROR"
            errors = [str(err)]
            results = []
        try:
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
            return content.task.task
        except Content.DoesNotExist:
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
            
            runtime = Runtime.objects.create(start=time.time(), task=task)
            runtime.save()
            content.save()

            task.status = status
            task.save()
        
            runtime.stop = time.time()
            runtime.total = runtime.stop - start
            runtime.save()

        return task_id

    
    async def _worker(self, fn:Callable, group: list) -> list:
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.workers) as executor:
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

        operator = partial(self._factoryze_operator, fn)
        manager = partial(self.start, operator)
        for ind in range(0, len(args), self.workers):
            yield manager(args[ind:ind+self.workers])