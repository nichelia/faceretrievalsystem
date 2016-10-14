#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# @author: Nicholas Elia
# @date:   Thu May 27 16:00:00 BST 2014

import bob
import scipy.spatial

from xfacereclib.paper.ne00021.BOVW import BOVW

# Setup of the BOVW face recognition algorithm as used in the LFW database
tool = BOVW(
    # pca_subspace_dimension     = float(0.95), # Using PCA Dimensionality Reduction of 95% accuracy.
    pca_subspace_dimension     = None,        # Using SIFT features - 128 Dimensions.
    # distance_function          = bob.math.chi_square,
    # distance_function          = bob.math.kullback_leibler,
    # is_distance_function       = True,   
    distance_function          = bob.math.histogram_intersection,
    is_distance_function       = False,
    kmeans_means               = float(0.05),  # Means will be equal to 1/20 of the feature space
    kmeans_iterations          = 4,
    kmeans_threshold           = 1e-5,
    sparse_histogram           = True,
    requires_inverted_indexing = True
)

# Face Recognition Algorithm (BOVW)