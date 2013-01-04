import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

description = ("simple django plugin for sending push messages"
               " from django server to sockjs clients"),

setup(
    name = "djazator",
    version = "0.1.1",
    author = "Mike Oskin",
    author_email = "cheap.grayhat@gmail.com",
    description = description,
    license = "MIT",
    keywords = "django zeromq tornado sockjs",
    packages = find_packages('src'),
    package_dir = {'':'src'},
    include_package_data = True,
    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst', '*.md'],
        },
    install_requires=['pyzmq>=2.0.0'],
    long_description=read('README.md'),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Framework :: Django"
    ],
)
