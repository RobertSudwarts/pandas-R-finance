#!/usr/bin/env python

from distutils.core import setup

setup(name='pandas-R-finance',
      version='1.0',
      description='R finance module/functions port for pandas',
      author='Robert Sudwarts',
      author_email='robert.sudwarts@gmail.com',
      url='',
      packages=['distutils', 'distutils.command'],
      install_requires=["pandas"],
      zip_safe=False,
      include_package_data=True,
      )
