# pyMatau

pyMatau is an OGC SensorThings API implementation in Python.

Detailed documentation is in the "docs" directory.

## Quick start

1. Install `pymatau` (e.g. `pip install pymatau/dist/pymatau-0.1.tar.gz`)

2. Add "pymatau" to your INSTALLED_APPS setting like this::

```buildoutcfg
INSTALLED_APPS = [
    ...
    'pymatau',
]
```

3. Also include the following Django Rest Framework settings in your settings.py file:

```buildoutcfg
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
    'URL_FIELD_NAME': 'selfLink',
    'ORDERING_PARAM': '$orderby',
    'DEFAULT_PAGINATION_CLASS': 'pymatau.query_options.SensorThingsPagination',
    'PAGE_SIZE': 100,
    'TEST_REQUEST_DEFAULT_FORMAT': 'json'
}
```

4. Include the pyMatau URLconf in your project urls.py like this::

```buildoutcfg
path('', include('pymatau.urls')),
```

5. Run `python manage.py migrate` to create the pyMatau (SensorThings) models.

6. Start the development server and visit http://127.0.0.1:8000/v1.0/


## tests

`python setup.py test`