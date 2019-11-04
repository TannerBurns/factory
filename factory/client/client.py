import requests

from typing import Any

class factoryclient:
    """facotryclient -- client class to interact with factory routes"""

    def __init__(self, url="http://127.0.0.1:8000", sessions: Any = []):
        self.taskurl = f'{url}/tasks'
        self.sessionurl = f'{url}/sessions'


    def taskids_from_session(self, session):
        resp = requests.get(f'{self.sessionurl}/{session}')
        if resp.status_code == 200:
            return [task.get('task') for task in resp.json().get('tasks', []) if task.get('task')]
        return []


                    



            


