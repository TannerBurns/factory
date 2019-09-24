Factory
=====

    A simple Django app to create and track different user defined tasks


Quick start
=====
    
    1. Pip install the factory django app (A python virtual environment is recommended)
        
        pip3 install .

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

    5. Run `python manage.py migrate` to create the factory models.


Examples
=====

Using factory in django project view

```python
from factory.factoryze import factoryze

def add(args):
    """add up the given arguments
    
    Arguments:
        args {list} -- list of numbers to add
    
    Returns:
        int -- total of all args
    """
    total = 0
    for x in args:
        total += x
    return total


class Testview(viewsets.ViewSet):
    """
    example viewset to use factory
    note: list method is used for an easy GET request viewset. can be used in any other methods
    """
    def list(self, request):
        client = factoryze(operators=4, workers=32, session="TestingSession")
        args = [(x,y) for x in range(0,10) for y in range(10, 20)]
        resp = client.factoryze(add, args)
        if resp:
            return Response(status=200)
        else:
            return Response(status=400)
```


Task List /tasks GET

```json
{
    "created": "2019-09-10T02:58:37.827669Z",
    "task": "a342614f-a349-4267-9798-d6c6159cb16a",
    "status": "COMPLETE",
    "session": "TestingSession",
    "operation": {
        "created": "2019-09-10T02:58:37.821612Z",
        "sha256": "c2b6275d61d5e00419208f529b28a4e1f5f70a32f1ebb9764be0af66c9c03430",
        "name": "add",
        "docstring": "add up the given arguments\n    \n    Arguments:\n        args {list} -- list of numbers to add\n    \n    Returns:\n        int -- total of all args\n    "
    },
    "runtime": {
        "created": "2019-09-10T02:58:37.846842Z",
        "start": 1568084317.8465128
    }
}
```

Task View /tasks/{task_uuid} GET

```json
{
    "created": "2019-09-10T02:58:37.827669Z",
    "task": "a342614f-a349-4267-9798-d6c6159cb16a",
    "status": "COMPLETE",
    "session": "TestingSession",
    "operation": {
        "created": "2019-09-10T02:58:37.821612Z",
        "sha256": "c2b6275d61d5e00419208f529b28a4e1f5f70a32f1ebb9764be0af66c9c03430",
        "name": "add",
        "docstring": "add up the given arguments\n    \n    Arguments:\n        args {list} -- list of numbers to add\n    \n    Returns:\n        int -- total of all args\n    "
    },
    "content": [
        {
            "created": "2019-09-10T02:58:37.840561Z",
            "errors": [],
            "results": [
                22,
                23,
                24,
                25,
                26,
                18,
                19,
                20,
                21,
                22,
                23,
                24,
                25,
                26,
                27,
                19,
                20,
                21,
                22,
                23,
                24,
                25,
                26,
                27,
                28
            ]
        }
    ],
    "runtime": {
        "created": "2019-09-10T02:58:37.846842Z",
        "start": 1568084317.8465128,
        "stop": 1568084317.859692,
        "total": 0.058561086654663086
    }
}
```
