# SensorAtlas

SensorAtlas is an OGC SensorThings API implementation in Python.

Detailed documentation is in the "docs" directory.

## Quick start

1. Install `sensorAtlas` (e.g. `pip install <path-to-file>/sensorAtlas-0.1.tar.gz`)

2. Add "sensoratlas" to your INSTALLED_APPS setting like this::

```buildoutcfg
INSTALLED_APPS = [
    ...
    'sensoratlas',
]
```

3. Also include the following Django Rest Framework settings in your settings.py file:

```buildoutcfg
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
    'URL_FIELD_NAME': 'selfLink',
    'ORDERING_PARAM': '$orderby',
    'DEFAULT_PAGINATION_CLASS': 'sensoratlas.query_options.SensorThingsPagination',
    'PAGE_SIZE': 100,
    'TEST_REQUEST_DEFAULT_FORMAT': 'json'
}
```

4. Include the sensoratlas URLconf in your project urls.py like this::

```buildoutcfg
path('api/', include('sensoratlas.urls')),
```

5. Run `python manage.py migrate` to create the sensorAtlas models.

6. Start the development server and visit http://127.0.0.1:8000/api/v1.0/

## Tests

`python setup.py test`
