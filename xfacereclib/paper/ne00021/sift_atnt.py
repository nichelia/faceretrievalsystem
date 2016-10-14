#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# @author: Nicholas Elia
# @date:   Thu May 27 16:00:00 BST 2014

from xfacereclib.paper.ne00021.VLSift import VLSift

# SIFT feature detector & descriptor as used in the AT&T database.
feature_extractor = VLSift(
  height      = 112,
  width       = 92,
  n_intervals = 3,
  n_octaves   = 5,
  octave_min  = 0,
  peak_thres  = 0.03,
  edge_thres  = 10.,
  magnif      = 3.
)

# Feature Extrator Algorithm (SIFT)