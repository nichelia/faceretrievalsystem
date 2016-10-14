#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# @author: Nicholas Elia
# @date:   Thu May 27 16:00:00 BST 2014

from setuptools import setup, find_packages

# The only thing done in this file is to call the setup() function with all parameters that define the package.
setup(

    # Basic Project Information:
    name='xfacereclib.paper.ne00021',
    version='1.0.0',
    description='Running the experiments as given in dissertation: "Face Retrieval System".',

    # Additional Project Information:
    url='http://github.com/nicholas-elia/xfacereclib-paper-frs2014', # Currently unavailable.
    license='LICENSE.txt',
    author='Nicholas Elia',
    author_email='nich.elia@gmail.com',

    # PyPI Description page:
    long_description=open('README.rst').read(),

    # Package Definition:
    packages=find_packages(),
    include_package_data=True,

    # Packages need to be installed in the current package.
    # All packages that are mentioned here, but are not installed on the current system will be installed locally and only visible to the scripts of this package.
    install_requires=[
      'setuptools',                   # the tool to install dependent packages.
      'bob >= 1.2.0, <= 1.3.0',       # the base signal processing/machine learning library containing most of the face recognition algorithms.
      'facereclib >= 1.2.1',          # the tool to actually run all experiments.
      'xbob.db.atnt',                 # the interface to the AT&T database.
      'xbob.db.lfw',                  # the interface to the LFW database.
      'matplotlib'                    # plotting utility.
    ],

    # Namespace Package.
    namespace_packages = [
      'xfacereclib',
      'xfacereclib.paper'
    ],

    # Registered Entry points (resources).
    entry_points = {
      # Register the console script, for executing the experiments.
      'console_scripts': [
        'ne00021_face_recog.py  = xfacereclib.paper.ne00021.execute:main',
      ],

      # Register particular databases as resources of FaceRecLib to be used on command line.
      'facereclib.database': [
        'c-atnt               = xfacereclib.paper.ne00021.database_atnt:database',
        'c-lfw-restricted     = xfacereclib.paper.ne00021.database_lfw:restricted',
        'c-lfw-unrestricted   = xfacereclib.paper.ne00021.database_lfw:unrestricted',
      ],
    },

    # Classifiers for PyPI
    classifiers = [
      'Development Status :: 1 - Beta',
      'Intended Audience :: Science/Research',
      'License :: ',
      'Natural Language :: English',
      'Programming Language :: Python :: 2.7',
      'Environment :: Console',
      'Framework :: Buildout',
      'Topic :: Scientific/Engineering',
    ],
)
