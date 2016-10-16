======================
Face Retrieval System
======================

This package provides the source code to run the experiments published in the final year project Face Retrieval System `report`_.
It relies on FaceRecLib_ and Bob_ in order to execute the face retrieval experiments.

.. note::
  Currently, this package only works in Unix-like environments and under MacOS.
  Due to limitations of the Bob_ library, MS Windows operating systems are not supported.
  A port of Bob_ for MS Windows is under work, but it is currently unavailable.
  In the meanwhile you could use the VirtualBox_ images that can be downloaded `here <http://www.idiap.ch/software/bob/images>`_.


Installation
============
The installation of this package relies on the `BuildOut <http://www.buildout.org>`_ system. By default, the following command line sequence should download and install almost all requirements, including the FaceRecLib_, the database interfaces `xbob.db.atnt <http://pypi.python.org/pypi/xbob.db.atnt>`_, `xbob.db.lfw <http://pypi.python.org/pypi/xbob.db.lfw>`_ and all their required packages.::

  $ python bootstrap.py
  $ ./bin/buildout


However there are a few exceptions:


Bob
---
The face recognition experiments rely on the open source signal-processing and machine learning toolbox Bob_.
To install Bob_, please visit `this link <http://www.idiap.ch/software/bob>`_ and follow the installation instructions.
Please verify that you have at least version 1.2.0 of Bob_ installed.
If you install Bob_ in a non-standard directory, please open the buildout.cfg file from the base directory and set the ``prefixes`` directory accordingly.

.. note::
  The experiments that are reported in this project were generated with Bob_ version 1.2.1 and FaceRecLib_ version 1.2.1.
  If you use different versions of either of these packages, the results might differ slightly.
  For example, due to some initialization differences, the results using Bob_ 1.2.0 and 1.2.1 are not identical, but similar.


Image Databases
---------------
The experiments are run on external image databases.
The images from the databases are not provided.
Hence, please contact the database owners to obtain a copy of the images.
The two databases used in our experiments can be downloaded here:

- `AT\&T <http://www.cl.cam.ac.uk/Research/DTG/attarchive:pub/data/att_faces.tar.Z>`_ [``atnt``]
- `LFW <http://vis-www.cs.umass.edu/lfw/lfw.tgz>`_ [``lfw``]

Important!
''''''''''
After downloading the databases, you will need to tell the software where it can find them by changing the **configuration files**.
In particular, please update the ``atnt_directory`` in **xfacereclib/paper/ne00021/database_atnt.py**, as well as the ``lfw_directory`` in **xfacereclib/paper/ne00021/database_lfw.py**.
Please let all other configuration parameters unchanged as this might influence the face retrieval experiments and hence, the reproducibility of the results.


Recreating the results of the project
====================================

After successfully setting up the databases, you are now able to run the face retrieval experiments as explained in the `report`_.

The experiment configuration
----------------------------
The face recognition experiments are run using the FaceRecLib_. For convenience there is a wrapper script that sets up the right parameters for the call to the FaceRecLib_.
The configuration files that are used by the FaceRecLib_, which contain all the parameters of the experiments, can be found in the **xfacereclib/paper/ne00021/** directory.

Running the experiments
-----------------------
This script can be found in ``bin/ne00021_face_recog.py``.
It requires some command line options, which you can list using ``./bin/ne00021_face_recog.py --help``.
Usually, the command line options have a long version (starting with ``--``) and a shortcut (starting with a single ``-``), here we use only the long versions:

- ``--temp-directory``: Specify a directory where temporary files will be stored (default: ``temp``). This directory can be deleted after all experiments ran successfully.
- ``--result-directory``: Specify a directory where final result files will be stored (default: ``results``). This directory is required to evaluate the experiments.
- ``--databases``: Specify a list of databases that you want your experiments to run on. Possible values are ``atnt`` and ``lfw``. By default, experiments are run on ``atnt``.
- ``--protocols``: Specify a list of protocols that you want to run. Possible values are ``view1``, ``fold1``, ``fold2`` , ``fold3``, ``fold4``, ``fold5``, ``fold6``, ``fold7``, ``fold8``, ``fold9`` and ``fold10`` for database ``lfw``, and none for ``atnt``. By default, ``view1`` is used for lfw. 
- ``--retrieval``: Defines the method to be used for retrieval. Possible values are ``codebook`` and ``dictionary``. By defualt ``codebook`` will be used.
- ``--verbose``: Print out additional information or debug information during the execution of the experiments. The ``--verbose`` option can be used several times, increasing the level to Warning (1), Info (2) and Debug (3). By default, only Error (0) messages are printed.
- ``--dry-run``: Use this option to print the calls to the FaceRecLib_ without executing them.

Additionally, you can pass options directly to the FaceRecLib_, but you should do that with care.
Simply use ``--`` to separate options to the ``bin/ne00021_face_recog.py`` from options to the FaceRecLib_.
For example, the ``--force`` option might be of interest.
See ``./bin/faceverify.py --help`` for a complete list of options.

It is advisable to use the ``--dry-run`` option before actually running the experiments, just to see that everything is set up correctly.
Also, the Info (2) verbosity level prints useful information, e.g. by adding the ``--verbose --verbose`` (or shortly ``-vv``) on the command line.
A commonly used command line sequence to execute the face recognition algorithm on both databases could be:

1. Run the experiments of BOVW codebook method on the ATNT database::

    $ ./bin/ne00021_face_recog.py -d atnt -m codebook -vvv

2. Run the experiments of BOVW proposed dictionary method on the ATNT database::

    $ ./bin/ne00021_face_recog.py -d atnt -m dictionary -vvv

3. Run the experiments of BOVW codebook method on the LFW database::

    $ ./bin/ne00021_face_recog.py -d lfw -p view1 -m codebook -vvv

4. Run the experiments of BOVW proposed dictionary method on the LFW database::

    $ ./bin/ne00021_face_recog.py -d lfw -p view1 -m dictionary -vvv

.. note::
  All the scripts' output directories are automatically generated if they do not exist yet.

.. warning::
  Scripts may take time to get executed and also require large amount of memory - especially the MOBIO database.
  Nevertheless, the scripts are set up in such a way so that they re-use parts of the experiments as much as possible.



Evaluating the experiments
--------------------------
After successful run of the experiments, the resulting score files can be evaluated.
For this, the ``bin/evaluate.py`` script can be used to create the Tables shown in Chapter 5 of the project `report`_.

Generating output files
'''''''''''''''''''''''

To run the script, some command line parameters have to be set, see ``./bin/evaluate.py --help``.

Again, the most usual way to compute the resulting tables could be:

1. Evaluate experiments on development set::

    $ ./bin/evaluate.py -d directory\_to\_scores-dev -R roc.pdf -D det.pdf -C cmc.pdf -c HTER

2. Evaluate experiments on evaluation set::

    $ ./bin/evaluate.py -e directory\_to\_scores-eval -R roc.pdf -D det.pdf -C cmc.pdf -c EER

.. note::
  It is required to delete the previous results in order to correctly compute new ones (if in the same directory).


.. _report: https://storage.googleapis.com/nichelia-storage/university/COM3001%20-%20Professional%20Project/finalreport.pdf
.. _idiap: http://www.idiap.ch
.. _bob: http://www.idiap.ch/software/bob
.. _facereclib: http://pypi.python.org/pypi/facereclib
.. _virtualbox: http://www.virtualbox.org
