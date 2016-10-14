#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# @author: Nicholas Elia
# @date:   Thu May 27 16:00:00 BST 2014

import facereclib
import argparse
import os
import pkg_resources
import sys

from xfacereclib.paper.ne00021 import faceverify
from xfacereclib.paper.ne00021 import faceverify_lfw


def command_line_options(command_line_parameters = None):
  # Set up command line parser.
  parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)

  parser.add_argument('-d', '--databases', nargs='+', choices = ('atnt', 'lfw'), default = ('atnt', 'lfw'),
      help = 'The databases to run experiments on.')

  parser.add_argument('-p', '--protocols', nargs='+', choices = ('view1', 'fold1', 'fold2', 'fold3', 'fold4', 'fold5', 'fold6', 'fold7', 'fold8', 'fold9', 'fold10'), default = ('view1'),
      help = 'The protocols to run; the protocols will automatically assigned to the according database.')

  parser.add_argument('-m', '--retrieval', default = ('codebook'),
      help = 'The methods to use for retrieval')

  parser.add_argument('-q', '--dry-run', action = 'store_true',
      help = 'Writes the actual call to the facereclib instead of executing it.')

  parser.add_argument('-T', '--temp-directory', default = 'temp',
      help = "The output directory for temporary files.")

  parser.add_argument('-R', '--result-directory', default = 'results',
      help = "The output directory for result files.")

  parser.add_argument('parameters', nargs = argparse.REMAINDER,
      help = "Parameters directly passed to the face verify script. Use -- to separate this parameters from the parameters of this script. See 'bin/faceverify.py --help' for a complete list of options.")

  # Add verbosity command line option.
  facereclib.utils.add_logger_command_line_option(parser)
  # Parse command line.
  args = parser.parse_args(command_line_parameters)
  # Set verbosity level.
  facereclib.utils.set_verbosity_level(args.verbose)

  # Return command line arguments.
  return args


PROTOCOLS = {
  'lfw' : ('view1', 'fold1', 'fold2', 'fold3', 'fold4', 'fold5', 'fold6', 'fold7', 'fold8', 'fold9', 'fold10'),
  'atnt': ('default')
}


def main():
  args = command_line_options(sys.argv[1:])
  # Get the directory, where the configuration files are stored.
  config_dir = os.path.dirname(pkg_resources.resource_filename('xfacereclib.paper.ne00021', 'execute.py'))

  # Iterate over all desired databases,
  for database in args.databases:
    # and over all protocols
    for protocol in args.protocols:
      # that fit to the database.
      if protocol in PROTOCOLS[database]:
        # Compute sub-directory for the experiments based on command line options.
        sub_directory = protocol
        # Get the correct database setup for the desired experiment.
        db = 'c-%s-%s' % (database, 'restricted') if database == 'lfw' else 'c-%s' % database
        # Get the method for retrieval.
        rm = '%s' % args.retrieval
        # Collect the parameters that will be sent to the bin/faceverify.py script,
        # which will finally execute the experiments.
        parameters = ['./bin/faceverify.py',
                      '--database', db,
                      '--protocol', protocol if database == 'lfw' else 'default',
                      '--preprocessing', 'face-crop',
                      '--features', os.path.join(config_dir, 'sift_%s.py' % database),
                      '--tool', os.path.join(config_dir, '%s_%s.py' % (rm, database)),
                      '--preprocessed-data-directory', '../preprocessed',
                      '--features-directory', '../features',
                      '--projector-file', '../Projector.hdf5',
                      '--projected-features-directory', '../projected',
                      '--temp-directory', os.path.join(args.temp_directory, database),
                      '--result-directory', os.path.join(args.result_directory, database),
                      '--sub-directory', sub_directory,
                      '--groups', 'dev'] #, 'world', '--calibrate-scores']

        # Set the verbosity level.
        if args.verbose:
          parameters.append('-' + 'v'*args.verbose)

        # Add the command line arguments that were specified on command line.
        if args.parameters:
          parameters.extend(args.parameters[1:])

        if args.dry_run:
          # Write what we would have executed.
          print "Would have executed:"
          print " ".join(parameters)
        else:
          # Write what we will execute.
          print "Launching:"
          print " ".join(parameters)
          # Execute the face recognition algorithm.
          faceverify.main(parameters) if database == 'atnt' else faceverify_lfw.main(parameters)


