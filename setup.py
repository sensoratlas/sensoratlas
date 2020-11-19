import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='sensoratlas',
    version='0.0.1',
    packages=['sensoratlas'],
    include_package_data=True,
    license='BSD-3-Clause',
    description='A Django app to serve sensor data with sensorthings API.',
    long_description=README,
    url='https://github.com/sensoratlas/sensoratlas',
    author='Joseph Percival',
    author_email='iosefa@georepublic.de',
    test_suite="runtests.runtests",
    python_requires=">=3.6",
    install_requires=[
        'boolean.py>=3.6',
        'djangorestframework>=3.9',
        'Django>=2.1',
        'psycopg2>=2.8.2',
        'djangorestframework-expander>=0.2.3',
        'python-dateutil>=2.8.0'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)