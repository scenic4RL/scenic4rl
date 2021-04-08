import os
from setuptools import setup


setup(
    name = "RL Training for Scenic-GFootball",
    version = "0.0.4",
    author = "Azad Salam",
    author_email = "salam_azad@berkeley.edu",
    description = ("An demonstration of how to create, document, and publish "
                                   "to the cheese shop a5 pypi.org."),
    license = "BSD",
    keywords = "example documentation tutorial",
    url = "http://packages.python.org/an_example_pypi_project",
    long_description="...",
    packages=['gfrl'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)