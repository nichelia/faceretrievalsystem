#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# @author: Nicholas Elia
# @date:   Thu May 27 16:00:00 BST 2014

import xbob.db.atnt
import facereclib

### IMPORTANT! ###

# Adapt the following directory:
# The directory where the images of the AT&T database is found
atnt_directory = "/home/bob/facedatabases/ORL"

# The database setup that is used by the FaceRecLib to compute the face recognition experiments
database = facereclib.databases.DatabaseXBob(
  database           = xbob.db.atnt.Database(),
  name               = "atnt",
  original_directory = atnt_directory,
  original_extension = ".pgm"
)

# Facial Database (AT&T)