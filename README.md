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

        path('your/route/', include('factory.urls')),

    5. Run `python manage.py migrate` to create the factory models.