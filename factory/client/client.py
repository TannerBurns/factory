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
        
    def get_results(self, taskid=None):
        if not self.sessions and not taskid:
            Exception("No parameters found to find results for, " \
            + "one of the following is required: session name, session id, or task id")
        results = []
        if taskid:
            # retrieve results for given taskid
            resp = self.get_task(taskid)
            if resp.status_code == 200:
                results.append([r for res in resp.json().get("content", []) for r in res.get("results", [])])
            else:
                results.append({"ERROR": "No results found", "status_code": resp.status_code})
        elif self.sessions:
            # get all results for given session
            taskids = []
            for session in self.sessions:
                taskids.extend(self.taskids_from_session(session))
            for tid in taskids:
                resp2 = self.get_task(tid)
                if resp2.status_code == 200:
                    results.extend([r.get("results") for r in resp2.json().get("content", [])])
                else:
                    results.append({"ERROR": "No results found", "status_code": resp.status_code, "task_id":tid})
        return [r for res in results for r in res if r]


                    



            


