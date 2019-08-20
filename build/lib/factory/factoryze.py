import os
import sys
import json
import time
import asyncio
import concurrent.futures

from functools import partial
from uuid import uuid4
from typing import Callable, Iterable, Tuple
from multiprocessing import Pool

from .models import Tasks

class factoryze:
    def __init__(self, operators=4, workers=16, session=str(uuid4())):
        self.operators = operators
        self.workers = workers
        self.session = session
    
    def start(self, fn: Callable, args: list) -> str:
        name = "UNKNOWN"
        try:
            name = fn.__name__
        except:
            try:
                name = fn.func.__name__
            except:
                pass
            pass
        task = Tasks.objects.create(
            name = name,
            session = self.session,
            start = time.time()
        )
        try:
            task.status = "IN PROGRESS"
            task.task_id = str(uuid4())
            task.save()
            rets = fn(args)
            task.status = "COMPLETE"
            try:
                if type(rets) != list:
                    rets = [rets]
                task.results = json.dumps(rets)
            except:
                task.results = json.dumps([rets])
        except Exception as err:
            task.status = "ERROR"
            task.errors = str(err)
        task.runtime = time.time() - task.start
        task.save()
        return task.task_id
    
    async def _worker(self, fn:Callable, group: list) -> list:
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.workers) as executor:
            loop = asyncio.get_event_loop()
            futures = [
                loop.run_in_executor(executor, partial(fn, item)) 
                for item in group if item
            ]
        await asyncio.gather(*futures)
        return [f.result() for f in futures]
    
    def _factoryze_operator(self, fn: Callable, args: list) -> list:
        loop = asyncio.get_event_loop()
        return [
            res
            for ind in range(0, len(args), self.workers)
            for res in loop.run_until_complete(
                self._worker(fn, args[ind:ind+self.workers])
            )
            if res
        ]
    
    def factoryze(self, fn: Callable, args: list) -> list:
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
        operator = partial(self._factoryze_operator, fn)
        manager = partial(self.start, operator)
        for ind in range(0, len(args), self.workers):
            yield manager(args[ind:ind+self.workers])