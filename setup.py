import os
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "Flask-ActivityPub",
    version = "0.0.1",
    author = "Steve Ivy",
    author_email = "steveivy@gmail.com",
    description = ("A toy implementation of ActivityPub for Flask applications"),
    license = "Mozilla Public License",
    url = "http://packages.python.org/an_example_pypi_project",
    packages=['flask_activitypub'],
    long_description=read('README.md'),
    install_requires=[
        "flask",
        "flask-restful",
        "activipy",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
    ],
)