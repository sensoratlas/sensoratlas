# SensorAtlas

SensorAtlas is a Django App that serves an OGC SensorThings API implementation in Python.

Detailed documentation is in the "docs" directory.

## Quick start

The following steps will explain how to add Sensor Atlas to an existing django application. If you do not
 have a django application, create one and install Sensor Atlas to get started. 

**NOTE: Sensor Atlas requires that django uses a PostGIS backend for its Database Settings.**

1. Install `sensorAtlas` (e.g. `pip install <path-to-file>/sensorAtlas-0.1.tar.gz`)

2. Add "sensorAtlas" to your INSTALLED_APPS setting like this (note `rest_framework` must be included in `INSTALLED_APPS`):

```
INSTALLED_APPS = [
    ...
    'rest_framework,
    'sensorAtlas',
]
```

3. Also include the following Django Rest Framework settings in your settings.py file:

```
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
    'URL_FIELD_NAME': 'selfLink',
    'ORDERING_PARAM': '$orderby',
    'DEFAULT_PAGINATION_CLASS': 'sensorAtlas.pagination.SensorThingsPagination',
    'PAGE_SIZE': 100,
    'TEST_REQUEST_DEFAULT_FORMAT': 'json'
}
```

4. Include the sensorAtlas URLconf in your project urls.py `urlpatterns` like this::

```
urlpatterns = [
    ...
    path('api/', include('sensorAtlas.urls')),
]
```

5. Run `python manage.py makemigrations sensorAtlas && python manage.py migrate` to create the sensorAtlas models.

6. Start the development server with `python manage.py runserver` and visit http://127.0.0.1:8000/api/v1.0/

## Tests

`python setup.py test`
