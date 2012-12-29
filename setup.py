import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

description = ("django server push messages through zeromq,"
               " tornado and tornado-sockjs"),

setup(
    name = "djazator",
    version = "0.1.0",
    author = "Mike Oskin",
    author_email = "cheap.grayhat@gmail.com",
    description = description,
    license = "BSD",
    keywords = "django zeromq tornado sockjs",
    packages = find_packages('src'),
    package_dir = {'':'src'},   # tell distutils packages are under src
    include_package_data = True,
    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst'],
        },
    long_description=read('README.rst'),
    classifiers=[
        "Development Status :: 1 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
