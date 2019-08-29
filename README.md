# pyMatau

pyMatau is an OGC SensorThings API implementation in Python.

Detailed documentation is in the "docs" directory.

## Quick start

1. Add "pymatau" to your INSTALLED_APPS setting like this::

```buildoutcfg
INSTALLED_APPS = [
    ...
    'pymatau',
]
```

2. Include the pyMatau URLconf in your project urls.py like this::

```buildoutcfg
path('polls/', include('polls.urls')),
```

3. Run `python manage.py migrate` to create the pyMatau (SensorThings) models.

4. Start the development server and visit http://127.0.0.1:8000/api/v1.0/
