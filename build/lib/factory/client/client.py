import requests

from typing import Any

class factoryclient:
    """facotryclient -- client class to interact with factory routes"""

    def __init__(self, url="http://127.0.0.1:8000", sessions: Any = []):
        self.baseurl = url
        self.taskurl = f'{url}/tasks'
        self.sessionurl = f'{url}/sessions'

        if type(sessions) == str:
            self.sessions = [sessions]
        elif type(sessions) == list:
            self.sessions = sessions
        else:
            self.session = []
    
    def get_task(self, taskid):
        return requests.get(f'{self.taskurl}/{taskid}')
    
    def taskids_from_session(self, session):
        taskids = []
        resp = requests.get(f'{self.sessionurl}/{session}')
        if resp.status_code == 200:
            response = resp.json()
            for r in response:
                taskids = [t.get("task") for t in r.get("tasks", [])]
        return taskids
        
    def get_task_results(self, taskid):
        resp = self.get_task(taskid)
        if resp.status_code == 200:
            cont = resp.json().get("content", [])
            return cont[0].get("results") if len(cont) > 0 else None
        else:
            return None

    def get_session_results(self):
        if self.sessions:
            # get all results for given session
            taskids = []
            for session in self.sessions:
                taskids.extend(self.taskids_from_session(session))
            for tid in taskids:
                resp = self.get_task(tid)
                if resp.status_code == 200:
                    cont = resp.json().get("content", [])
                    yield cont[0].get("results") if len(cont) > 0 else None
                else:
                   yield None


                    



            


