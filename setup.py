#!/usr/bin/env python
from setuptools import setup
import sys

py_entry = 'pypd%s = pypd.main:main'
# pycompleter_entry = 'pycompleter%s = pythonpy.pycompleter:main'
endings = ('', sys.version[:1], sys.version[:3])
entry_points_scripts = []
for e in endings:
    entry_points_scripts.append(py_entry % e)
    # entry_points_scripts.append(pycompleter_entry % e)

setup(
    name='pypd',
    version='0.1.0',
    description='The command line version of Pandas(Python Data Analysis Library)',
    #data_files=data_files,
    license='MIT',
    url='https://github.com/cangfengzhe/pypd',
    long_description='https://github.com/cangfengzhe/pypd',
    packages=['pypd'],
    # package_data={'pythonpy': ['completion/pycompletion.sh']},
    scripts=['pypd/main.py'],
    entry_points = {
        'console_scripts': entry_points_scripts
    },
)
