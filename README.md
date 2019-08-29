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

3. Include the pyMatau URLconf in your project urls.py like this::

```buildoutcfg
path('polls/', include('polls.urls')),
```

4. Run `python manage.py migrate` to create the pyMatau (SensorThings) models.

5. Start the development server and visit http://127.0.0.1:8000/api/v1.0/


## tests

`python setup.py test`