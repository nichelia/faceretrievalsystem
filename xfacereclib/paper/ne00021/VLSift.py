#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# @author: Nicholas Elia
# @date:   Thu May 27 16:00:00 BST 2014

import bob
import os
import numpy
import re
import math
from facereclib import utils
from xfacereclib.paper.ne00021.features import Extractor


class VLSift(Extractor):
  """Use of SIFT algorithm to detect interesting/discriminative points and extract descriptors of those keypoints"""

  def __init__(
      self,
      height,
      width,
      n_intervals,
      n_octaves,
      octave_min,
      peak_thres,
      edge_thres,
      magnif):

    # Call base class constructor.
    Extractor.__init__(self),
                       # requires_training             = True,
                       # split_training_data_by_client = True)

    # Prepare SIFT extractor.
    self.m_height      = height
    self.m_width       = width
    self.m_n_intervals = n_intervals
    self.m_n_octaves   = n_octaves
    self.m_octave_min  = octave_min
    self.m_peak_thres  = peak_thres
    self.m_edge_thres  = edge_thres
    self.m_magnif      = magnif

    # SIFT extractor
    self.m_sift_extract = bob.ip.VLSIFT(self.m_height, self.m_width, self.m_n_intervals, self.m_n_octaves, self.m_octave_min, self.m_peak_thres, self.m_edge_thres, self.m_magnif)

  # def __match_sift_points(self, image1, image2):
  #   """Compares two images' SIFT features to see which match. The ones that do not match anywhere, are discarded."""

  #   # Normalize each input vector to unit length.
  #   image1 = image1 / numpy.sqrt(numpy.sum((image1)**2))
  #   image2 = image2 / numpy.sqrt(numpy.sum((image2)**2))

  #   # Keep the matches where vector angles from
  #   # nearest to second nearest neighnor is less than the threshold.
  #   threshold = 0.6;
  #   image2T = image2.conj().T
  #   match = numpy.zeros(image1.shape[0], dtype=numpy.int)
  #   for i in range(image1.shape[0]):
  #     # compute vector of dot products
  #     dotproduct = numpy.dot(image1[i,:],image2T)
  #     # take inverse cosine and sort results
  #     vals = numpy.sort(numpy.arccos(dotproduct))
  #     indx = numpy.argsort(numpy.arccos(dotproduct))

  #     # Check if nearest neighbor has angle less than threshlold times 2nd.
  #     if (vals[0] < threshold * vals[1]):
  #       match[i] = indx[0]

  #   return

  # def __compare_client_images__(self, images):
  #   """Compares all images of the client and returns the most discriminative SIFT features"""

  #   # Loop through all the image files.
  #   self.__match_sift_points(numpy.vstack(images[0]), numpy.vstack(images[7]))

  #   return

  # def __separate_descriptor__(self, feature):
  #   """Separates the descriptor from the keypoints"""
  #   l_key  = 4            # Length of SIFT keypoint.
  #   l_desc = 128          # Length of the SIFT descriptors.
  #   l_feat = len(feature) # Length of feature.

  #   sift_keypoints  = numpy.ndarray(shape=(l_feat,l_key), dtype=feature[0].dtype)
  #   sift_descriptor = numpy.ndarray(shape=(l_feat,l_desc), dtype=feature[0].dtype)

  #   # Separate the keypoints and the descriptors.
  #   k=0
  #   for val in feature:
  #     sift_keypoints[k]  = val[0:4]
  #     sift_descriptor[k] = val[4:]
  #     k=k+1

  #   return sift_descriptor


  # def train(self, image_list, extractor_file, image_files):
  #   """Trains the SIFT extractor so only matched points are saved for every client"""

  #   # Write data to the file.
  #   f = bob.io.HDF5File(extractor_file,"w")

  #   i = 0
  #   # For every client in the image list,
  #   for client in image_list:
  #     client_features_list = []
  #     # and for every image of the client,
  #     for image in client:
  #       # extract sift features.
  #       imageToProcess = numpy.vstack(image)
  #       self.imageFeatures = self.__separate_descriptor__(self.m_sift_extract(imageToProcess.astype('uint8')))
  #       client_features_list.append(self.imageFeatures)
  #     # Since all features are collected, do SIFT matching to find
  #     # the most discriminant features of the client.
  #     client_matches = self.__compare_client_images__(client_features_list)
  #     # Finally, save the matched sift features.
  #     for image_directory in image_files[i]:
  #       f.set(re.sub(r'\/', '', image_directory), self.imageFeatures)
  #     i = i + 1


  # def load(self, extractor_file):
  #   """Read the data saved in the file"""
  #   # Read data from the file.
  #   f = bob.io.HDF5File(extractor_file)

  def save_feature(self, feature, feature_file):
    """Save extracted SIFT features separated into keypoints and descriptors"""
    utils.ensure_dir(os.path.dirname(feature_file))

    l_key  = 4            # Length of SIFT keypoint.
    l_desc = 128          # Length of the SIFT descriptors.
    l_feat = len(feature) # Length of feature.

    sift_keypoints  = numpy.ndarray(shape=(l_feat,l_key), dtype=feature[0].dtype)
    sift_descriptor = numpy.ndarray(shape=(l_feat,l_desc), dtype=feature[0].dtype)

    # Separate the keypoints and the descriptors.
    k=0
    for val in feature:
      sift_keypoints[k]  = val[0:4]
      sift_descriptor[k] = val[4:]
      k=k+1

    # For this implementation, only descriptors are needed.
    bob.io.save(sift_descriptor, feature_file)

  def __call__(self, image, image_file):
    """Find and describe SIFT features on a given image"""

    imageToProcess = image.astype('uint8')

    # Extract and return descriptors.
    return self.m_sift_extract(imageToProcess)

