# flake8: noqa
import os
# from codecs import open as codecs_open
from setuptools import setup

HERE = os.path.abspath(os.path.dirname(__file__))

##############################
##  DO NOT TOUCH THIS FILE  ##
##############################

# Setup the assignment
setup(
    name="de-assignment-v1",
    version="0.1.0",
    url="https://gitlab.com/nascentxyz/de-assignment-v1",
    author="Jeffrey Wan",
    author_email="Jwan622@gmail.com",
    license="MIT License",
    package_dir={"": "assignment"},
    entry_points={"console_scripts": ["db_import=assignment:ingest"]},
    install_requires=[
        "sqlalchemy==1.2.13",
        "beautifulsoup4",
        "requests",
        'pytest-dotenv',
        'typer',
        'psycopg2',
    ],
    tests_require=[
        "pytest",
        "black",
        "flake",
        "pytest-mock",
        'pytest-dotenv'
    ],
)
