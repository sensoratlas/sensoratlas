import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='pymatau',
    version='0.1',
    packages=['pymatau'],
    include_package_data=True,
    license='MIT License',
    description='An OGC SensorThings API implementation in Python.',
    long_description=README,
    url='https://www.example.com/',
    author='Joseph Percival',
    author_email='ipercival@gmail.com',
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