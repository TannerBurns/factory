Factory
=====

![Python3.7 badge](https://img.shields.io/badge/python-v3.7-blue)

    A simple Django app to create and track different user defined tasks


Quick start
=====
    
    1. Pip install the factory django app (A python virtual environment is recommended)
        
        pip3 install .

        includes: factory, django, django-rest-framework, django-filter, psycopg2 (now required due to concurrency)

    2. Add "factory" to your INSTALLED_APPS settings like this:

        INSTALLED_APPS = [
            ...
            'rest_framework',
            'django_filters',
            'factory'
        ]
    
    3. Add the following the bottom of your project settings:

        REST_FRAMEWORK = {
            'DEFAULT_PARSER_CLASSES': [
                'rest_framework.parsers.FormParser',
                'rest_framework.parsers.MultiPartParser',
                'rest_framework.parsers.JSONParser',
            ],
            'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
            'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
            'PAGE_SIZE': 25,
        }

    4. Include the factory URLconf in your project urls.py like this:

        from django.urls import path, include

        path('your/route/', include('factory.urls')),
    
    5. (Now Required) Use PostgreSQL backend, replace the following in your project settings:

        NAME, USER, and PASSWORD need to be replaced with valid credentials

        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': 'dbname',
                'USER': 'username',
                'PASSWORD': 'password',
                'HOST': 'localhost',
                'PORT': '',
            }
        }

    6. Run `python manage.py migrate` to create the factory models.


Examples
=====

Using factory in django project view

```python
from rest_framework.response import Response
from rest_framework import viewsets
from threading import Thread

from factory.factoryze import factoryze

def add(x, y):
   return x+y


class Testview(viewsets.ViewSet):
    def list(self, request):
        client = factoryze(operators=4, workers=32)
        args = [([x,y], ) for x in range(0,250) for y in range(250,500)]
        Thread(target=client.factoryze, args=(add, args, )).start()
        return Response(status=200)
    
```


Task List /tasks GET

```json
{
    "count": 8,
    "next": null,
    "previous": null,
    "results": [
        {
            "created": "2019-09-28T06:18:48.139616Z",
            "task": "44247b5e-f4e5-4fc9-b68c-016cc1740fba",
            "status": "COMPLETE",
            "sessions": [
                {
                    "created": "2019-09-28T06:18:48.118956Z",
                    "name": "factoryze-client-1569651518-4316318",
                    "session_id": "3f6cd982-76e4-4f66-b391-c1b926a55434"
                },
                {
                    "created": "2019-09-28T06:19:20.600954Z",
                    "name": "factoryze-client-1569651556-617643",
                    "session_id": "0323e6b6-c197-47b0-a28c-f9b0f6e075fc"
                }
            ],
            "operation": {
                "created": "2019-09-28T06:18:48.125598Z",
                "sha256": "c319283f80706a7ed27396bc51a06f11595c8a6d4270171a54e0d7ce584e01bc",
                "name": "add",
                "docstring": "add up the given arguments\n    \n    Arguments:\n        args {list} -- list of numbers to add\n    \n    Returns:\n        int -- total of all args\n    "
            },
            "runtime": {
                "created": "2019-09-28T06:18:48.157557Z",
                "start": 1569651528.15704
            }
        },
        ...
        {
            "created": "2019-09-28T06:33:55.846639Z",
            "task": "67c6a83b-df2d-4414-84ef-009ed5fdff3a",
            "status": "COMPLETE",
            "sessions": [
                {
                    "created": "2019-09-28T06:33:55.824488Z",
                    "name": "factoryze-client-1569652431-4430878",
                    "session_id": "00bf65ce-30fd-4768-b14b-93567fd98694"
                }
            ],
            "operation": {
                "created": "2019-09-28T06:33:55.831959Z",
                "sha256": "fc0572946dfd4362652bfee65d04ae3926bb697fd45b3a415efa666185e7edb8",
                "name": "add",
                "docstring": "add up the given arguments\n    \n    Arguments:\n        args {list} -- list of numbers to add\n    \n    Returns:\n        int -- total of all args\n    "
            },
            "runtime": {
                "created": "2019-09-28T06:33:55.860129Z",
                "start": 1569652435.85966
            }
        }
    ]
}
```

Task View /tasks/{task_uuid} GET

```json
{
    "created": "2019-09-28T06:33:55.846639Z",
    "task": "67c6a83b-df2d-4414-84ef-009ed5fdff3a",
    "status": "COMPLETE",
    "sessions": [
        {
            "created": "2019-09-28T06:33:55.824488Z",
            "name": "factoryze-client-1569652431-4430878",
            "session_id": "00bf65ce-30fd-4768-b14b-93567fd98694"
        }
    ],
    "operation": {
        "created": "2019-09-28T06:33:55.831959Z",
        "sha256": "fc0572946dfd4362652bfee65d04ae3926bb697fd45b3a415efa666185e7edb8",
        "name": "add",
        "docstring": "add up the given arguments\n    \n    Arguments:\n        args {list} -- list of numbers to add\n    \n    Returns:\n        int -- total of all args\n    "
    },
    "content": [
        {
            "created": "2019-09-28T06:33:55.876947Z",
            "errors": [],
            "results": [
                15,
                16,
                17,
                18,
                19,
                20,
                21,
                22,
                23,
                24,
                16,
                17,
                18,
                19,
                20,
                21,
                22,
                23,
                24,
                25,
                17,
                18,
                19,
                20,
                21
            ]
        }
    ],
    "runtime": {
        "created": "2019-09-28T06:33:55.860129Z",
        "start": 1569652435.85966,
        "stop": 1569652435.88495,
        "total": 0.081866979598999
    }
}
```

Sessions List /sessions GET

```json
{
    "count": 3,
    "next": null,
    "previous": null,
    "results": [
        {
            "created": "2019-09-28T06:18:48.118956Z",
            "name": "factoryze-client-1569651518-4316318",
            "session_id": "3f6cd982-76e4-4f66-b391-c1b926a55434",
            "tasks": [
                {
                    "created": "2019-09-28T06:18:48.139616Z",
                    "task": "44247b5e-f4e5-4fc9-b68c-016cc1740fba",
                    "status": "COMPLETE",
                    "operation": {
                        "created": "2019-09-28T06:18:48.125598Z",
                        "sha256": "c319283f80706a7ed27396bc51a06f11595c8a6d4270171a54e0d7ce584e01bc",
                        "name": "add",
                        "docstring": "add up the given arguments\n    \n    Arguments:\n        args {list} -- list of numbers to add\n    \n    Returns:\n        int -- total of all args\n    "
                    },
                    "runtime": {
                        "created": "2019-09-28T06:18:48.157557Z",
                        "start": 1569651528.15704
                    }
                },
                ...
                {
                    "created": "2019-09-28T06:18:48.138611Z",
                    "task": "835f0787-0d97-446a-aeb9-3bd0f977c686",
                    "status": "COMPLETE",
                    "operation": {
                        "created": "2019-09-28T06:18:48.125598Z",
                        "sha256": "c319283f80706a7ed27396bc51a06f11595c8a6d4270171a54e0d7ce584e01bc",
                        "name": "add",
                        "docstring": "add up the given arguments\n    \n    Arguments:\n        args {list} -- list of numbers to add\n    \n    Returns:\n        int -- total of all args\n    "
                    },
                    "runtime": {
                        "created": "2019-09-28T06:18:48.156309Z",
                        "start": 1569651528.15598
                    }
                }
            ]
        },
        {
            "created": "2019-09-28T06:19:20.600954Z",
            "name": "factoryze-client-1569651556-617643",
            "session_id": "0323e6b6-c197-47b0-a28c-f9b0f6e075fc",
            "tasks": [
                ...
            ]
        },
        {
            "created": "2019-09-28T06:33:55.824488Z",
            "name": "factoryze-client-1569652431-4430878",
            "session_id": "00bf65ce-30fd-4768-b14b-93567fd98694",
            "tasks": [
                ...
            ]
        }
    ]
}
```

Session List /sessions/{name or session_id} GET

```json
[
    {
        "created": "2019-09-28T06:33:55.824488Z",
        "name": "factoryze-client-1569652431-4430878",
        "session_id": "00bf65ce-30fd-4768-b14b-93567fd98694",
        "tasks": [
            {
                "created": "2019-09-28T06:33:55.838777Z",
                "task": "5fe45f18-94cd-4116-88a6-ba08f5d6a08f",
                "status": "COMPLETE",
                "operation": {
                    "created": "2019-09-28T06:33:55.831959Z",
                    "sha256": "fc0572946dfd4362652bfee65d04ae3926bb697fd45b3a415efa666185e7edb8",
                    "name": "add",
                    "docstring": "add up the given arguments\n    \n    Arguments:\n        args {list} -- list of numbers to add\n    \n    Returns:\n        int -- total of all args\n    "
                },
                "runtime": {
                    "created": "2019-09-28T06:33:55.852982Z",
                    "start": 1569652435.85268
                }
            },
            ...
            {
                "created": "2019-09-28T06:33:55.845885Z",
                "task": "64d4ff98-f352-417f-82e1-7d7520820368",
                "status": "COMPLETE",
                "operation": {
                    "created": "2019-09-28T06:33:55.831959Z",
                    "sha256": "fc0572946dfd4362652bfee65d04ae3926bb697fd45b3a415efa666185e7edb8",
                    "name": "add",
                    "docstring": "add up the given arguments\n    \n    Arguments:\n        args {list} -- list of numbers to add\n    \n    Returns:\n        int -- total of all args\n    "
                },
                "runtime": {
                    "created": "2019-09-28T06:33:55.860533Z",
                    "start": 1569652435.86017
                }
            }
        ]
    }
]
```