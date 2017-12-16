#!/usr/bin/env python

from distutils.core import setup

setup(name='keytest',
      version='0.1.0',
      packages=['keytest'],
      install_requires=[
          'cryptography',
          'colorama',
          'termcolor',
      ],
      entry_points={
          'console_scripts' : [
              'keytest=keytest.command_line:main'
          ],
      },
     )
