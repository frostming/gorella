#!/usr/bin/env python
import os
import re
from setuptools import setup


def get_version():
    content = open('gorella.py').read()
    return re.findall(r'__version__\s*=\s*[\'"](.+?)[\'"]', content, re.M)[0]


setup(
    name='gorella',
    version=get_version(),
    description='Monkey patch regular expressions',
    long_description=open('README.md').read(),
    author='Frost Ming',
    author_email='mianghong@gmail.com',
    url='https://github.com/frostming/gorella',
    py_modules=['gorella'],
    license='MIT'
)
