#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# @author: Nicholas Elia
# @date:   Thu May 27 16:00:00 BST 2014

import xbob.db.lfw
import facereclib

### IMPORTANT! ###

# Adapt the following directory:
# The directory where the images of the LFW database is found
lfw_directory = "/home/bob/facedatabases/LFW"

restricted = facereclib.databases.DatabaseXBob(
    database           = xbob.db.lfw.Database(),
    name               = 'lfw',
    original_directory = lfw_directory,
    original_extension = ".jpg",
    protocol           = 'view1',

    all_files_options          = {'world_type' : 'restricted'},
    extractor_training_options = {'world_type' : 'restricted'}, # 'subworld' : 'twofolds'
    projector_training_options = {'world_type' : 'restricted'}, # 'subworld' : 'twofolds'
    enroller_training_options  =  {'world_type' : 'restricted'} # 'subworld' : 'twofolds'
)

unrestricted = facereclib.databases.DatabaseXBob(
    database           = xbob.db.lfw.Database(),
    name               = 'lfw',
    original_directory = lfw_directory,
    original_extension = ".jpg",
    protocol           = 'view1',

    all_files_options          = {'world_type' : 'unrestricted'},
    extractor_training_options = {'world_type' : 'unrestricted'}, # 'subworld' : 'twofolds'
    projector_training_options = {'world_type' : 'unrestricted'}, # 'subworld' : 'twofolds'
    enroller_training_options  =  {'world_type' : 'unrestricted'} # 'subworld' : 'twofolds'
)

# Facial Database (LFW)