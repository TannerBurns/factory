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
            args = [(x,y) for x in range(0,8) for y in range(8, 16)]
            resp = client.factoryze(add, args)
            if resp:
                return Response(status=200)
            else:
                return Response(status=400)
    ```


    Task List /tasks GET

    ```json
    {
        "created": "2019-09-09T03:33:50.084662Z",
        "task": "64f705b5-d416-4a79-8518-a272b9ebc0ea",
        "status": "COMPLETE",
        "session": "TestingSession",
        "operation": {
            "created": "2019-09-09T03:33:50.071129Z",
            "sha256": "cf60b1eec981d900a4f0281a2ede0c751f2a958d04d9e3382ff894ec371d9fa0",
            "name": "add",
            "docstring": "add up the given arguments\n    \n    Arguments:\n        args {list} -- list of numbers to add\n    \n    Returns:\n        int -- total of all args\n    "
        },
        "content": {
            "created": "2019-09-09T03:33:50.110943Z",
            "input": {
                "created": "2019-09-09T03:33:50.101003Z",
                "sha256": "db2f3da3eb35b6bc772b68937fcd096552b573dc07ffc5c44aae5340a0e6a1a7",
                "count": 16
            },
            "output": {
                "created": "2019-09-09T03:33:50.106556Z",
                "sha256": "5cc76a93e727e197fe99fbe8b5ff6b262e21b6aa619091f550d8f465340b413b",
                "count": 16
            }
        },
        "runtime": {
            "created": "2019-09-09T03:33:50.087638Z",
            "start": 1568000030.087261
        }
    }
    ```

    Task View /tasks/64f705b5-d416-4a79-8518-a272b9ebc0ea GET

    ```json
    {
        "created": "2019-09-09T03:33:50.084662Z",
        "task": "64f705b5-d416-4a79-8518-a272b9ebc0ea",
        "status": "COMPLETE",
        "session": "TestingSession",
        "operation": {
            "created": "2019-09-09T03:33:50.071129Z",
            "sha256": "cf60b1eec981d900a4f0281a2ede0c751f2a958d04d9e3382ff894ec371d9fa0",
            "name": "add",
            "docstring": "add up the given arguments\n    \n    Arguments:\n        args {list} -- list of numbers to add\n    \n    Returns:\n        int -- total of all args\n    "
        },
        "content": {
            "created": "2019-09-09T03:33:50.110943Z",
            "input": {
                "created": "2019-09-09T03:33:50.101003Z",
                "sha256": "db2f3da3eb35b6bc772b68937fcd096552b573dc07ffc5c44aae5340a0e6a1a7",
                "type": "<class 'tuple'>",
                "count": 16
            },
            "output": {
                "created": "2019-09-09T03:33:50.106556Z",
                "sha256": "5cc76a93e727e197fe99fbe8b5ff6b262e21b6aa619091f550d8f465340b413b",
                "count": 16,
                "errors": [],
                "results": [
                    10,
                    11,
                    12,
                    13,
                    14,
                    15,
                    16,
                    17,
                    11,
                    12,
                    13,
                    14,
                    15,
                    16,
                    17,
                    18
                ]
            }
        },
        "runtime": {
            "created": "2019-09-09T03:33:50.087638Z",
            "start": 1568000030.087261,
            "stop": 1568000030.117734,
            "total": 0.05488181114196777
        }
    }
    ```
