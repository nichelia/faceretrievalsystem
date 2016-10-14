#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# @author: Nicholas Elia
# @date:   Thu May 27 16:00:00 BST 2014

import bob
import numpy
import scipy.spatial
try: reduce
except: from functools import reduce

from facereclib import utils
from xfacereclib.paper.ne00021.Tool import Tool

class BOVW (Tool):
  """Tool for computing inverted file using KMeans"""

  def __init__(
      self,
      pca_subspace_dimension,  # if int, number of subspace dimensions; if float, percentage of variance to keep (if None no PCA to be used).
      distance_function,
      is_distance_function,
      kmeans_means,            # if int, number of clusters; if float, percentage of the feature space to be used as clusters.
      kmeans_iterations,
      kmeans_threshold,
      sparse_histogram,
      requires_inverted_indexing,
      **kwargs                 # parameters directly sent to the base class
  ):

    """Initializes the BOVW tool with the given setup"""
    # Call base class constructor and register that the tool performs a projection.
    Tool.__init__(
        self,
        performs_projection        = True,
        pca_subspace_dimension     = pca_subspace_dimension,
        distance_function          = str(distance_function),
        is_distance_function       = is_distance_function,
        kmeans_means               = kmeans_means,
        kmeans_iterations          = kmeans_iterations,
        kmeans_threshold           = kmeans_threshold,
        sparse_histogram           = sparse_histogram,
        requires_inverted_indexing = requires_inverted_indexing,
        **kwargs
    )

    self.m_subspace_dim               = pca_subspace_dimension
    self.m_distance_function          = distance_function
    self.m_factor                     = -1 if is_distance_function else 1.
    self.m_kmeans_means               = kmeans_means
    self.m_kmeans_training_iterations = kmeans_iterations
    self.m_kmeans_training_threshold  = kmeans_threshold
    self.m_sparse_histogram           = sparse_histogram
    self.m_requires_inverted_indexing = requires_inverted_indexing


  def __train_pca__(self, feature_space):
    """Generates the PCA covariance matrix"""
    
    # Initializes the data to apply PCA on.
    data_list = []
    for client in feature_space:
      for feature in client:
        data_list.append(feature)
    data = numpy.vstack(data_list)
    del data_list

    utils.info("  -> Training LinearMachine using PCA")

    # Training.
    t = bob.trainer.PCATrainer()
    machine, variances = t.train(data)
    del data

    # Compute variance percentage, if desired.
    if isinstance(self.m_subspace_dim, float):
      cummulated = numpy.cumsum(variances) / numpy.sum(variances)
      for index in range(len(cummulated)):
        if cummulated[index] > self.m_subspace_dim:
          self.m_subspace_dim = index
          break
      self.m_subspace_dim = index
      del cummulated

    utils.info("    ... Keeping %d PCA dimensions" % self.m_subspace_dim)

    # Re-shape machine.
    machine.resize(machine.shape[0], self.m_subspace_dim)
    variances.resize(self.m_subspace_dim)

    # Return machine.
    return machine, variances


  def __perform_pca__(self, machine, client):
    """Perform PCA on the client"""

    # Allocates an array for the PCA projected data.
    client_data_list = []

    # Projects the data to the new PCA feature space (every keypoint descriptor of the image file).
    for feature in client:
      projected_feature = numpy.ndarray(machine.shape[1], numpy.float64)
      machine(feature, projected_feature)
      client_data_list.append(projected_feature)
    client_data = numpy.vstack(client_data_list)
    del client_data_list

    # Return the projected data.
    return client_data


  def __pca_feature_space__(self, machine, feature_space):
    """Perform PCA on data"""

    # The data of the new feature space.
    data = []
    for client in feature_space:
      data.append(self.__perform_pca__(machine, client))

    # Return the new feature space.
    return data


  def __train_kmeans__(self, feature_space):
    """Compute KMeans classification of the data"""

    utils.info("  -> Training KMeans")

    # Form the feature space for training KMeans.
    data_list = []
    for client in feature_space:
      for feature in client:
        data_list.append(feature)
    data = numpy.vstack(data_list)
    del data_list

    # Compute the number of clusers of KMeans.
    global m_kmeans_means
    self.m_kmeans_means = numpy.uint32(data.shape[0] * self.m_kmeans_means) if isinstance(self.m_kmeans_means, float) else self.m_kmeans_means

    # Machine.
    dimension = feature_space[0].shape[1]
    kmeans    = bob.machine.KMeansMachine(self.m_kmeans_means, dimension)

    # Training.
    t                       = bob.trainer.KMeansTrainer()
    t.max_iterations        = self.m_kmeans_training_iterations
    t.convergence_threshold = self.m_kmeans_training_threshold
    
    t.train(kmeans, data)
    del data

    # Return machine.
    return kmeans


  def __compute_histogram__(self, machine, client):
    """Compute the histogram of KMeans variances for each client"""
    
    # Clear the means that include any NaN (not a number) values.
    means = machine.means[~numpy.isnan(machine.means).any(1)]

    # For every cluster in KMeans space,
    distance_to_clusters_list = []
    for cluster in means:
      # compute Euclidean distance of client's features to this cluster.
      distance_value = client - numpy.tile(cluster, (client.shape[0],1))
      distance_value = numpy.sqrt(numpy.sum((distance_value)**2, axis=1))
      distance_to_clusters_list.append(distance_value)
    data = numpy.vstack(distance_to_clusters_list)
    del distance_to_clusters_list

    # Find the minimum distance to clusters of a feature.
    minimum_distance = numpy.amin(data, axis=0)

    # Mark the minimum distances to the data collected.
    data = numpy.float64(data==numpy.tile(minimum_distance,(data.shape[0],1)))

    # Mark the cluster of the minimum distance.
    for n in range (means.shape[0]):
      data[n,:] = data[n,:]*(n+1)
    classification = data.max(0)
    del data

    hist, bin_edges = numpy.histogram(classification, bins=means.shape[0])
    hist = numpy.float64(hist)
    hist = hist / numpy.sum(hist)
    del classification

    # Determine the use of sparse histogram.
    hist = utils.histogram.sparsify(hist) if self.m_sparse_histogram else hist

    return hist


  def train_projector(self, training_features, projector_file):
    """Generate required Machines for training"""

    # Create PCA machine if dimensionality reduction selected.
    if self.m_subspace_dim is not None:
      self.m_pca_machine, self.m_pca_eigenvalues = self.__train_pca__(training_features)
      training_features = self.__pca_feature_space__(self.m_pca_machine, training_features)
    # Create KMeans machine.
    self.m_kmeans_machine = self.__train_kmeans__(training_features)

    # Write machine(s) to file.
    f = bob.io.HDF5File(projector_file, "w")
    # Include all the PCA related files if dimensionality reduction is selected.
    if self.m_subspace_dim is not None:
      f.create_group("/pca")
      f.cd("/pca")
      f.set("Eigenvalues", self.m_pca_eigenvalues)
      f.create_group("Machine")
      f.cd("/pca/Machine")
      self.m_pca_machine.save(f)
    # Include all the KMeans related files.
    f.create_group("/kmeans")
    f.cd("/kmeans")
    f.create_group("Machine")
    f.cd("/kmeans/Machine")
    self.m_kmeans_machine.save(f)


  def load_projector(self, projector_file):
    """Read data from the Machines generated"""

    # Read machine(s) from file.
    f = bob.io.HDF5File(projector_file)
    # Read all the PCA related files if dimensionality reduction is selected.
    if self.m_subspace_dim is not None:
      f.cd("/pca")
      self.m_pca_eigenvalues = f.read("Eigenvalues")
      f.cd("/pca/Machine")
      self.m_pca_machine = bob.machine.LinearMachine(f)
    # Read all the KMeans related files.
    f.cd("/kmeans")
    f.cd("/kmeans/Machine")
    self.m_kmeans_machine = bob.machine.KMeansMachine(f) 


  def project(self, feature):
    """Projects the data"""

    # Project the data to a new feature space (using PCA dimensionality reduction).
    if self.m_subspace_dim is not None:
      feature = self.__perform_pca__(self.m_pca_machine, feature)
    # Compute a histogram for the data in the feature space according to KMeans.
    feature = self.__compute_histogram__(self.m_kmeans_machine, feature)

    return feature


  def enroll(self, enroll_features):
    """Enrolls the model by computing the average of all features"""
   
    if self.m_sparse_histogram:
      # Get all indices for the sparse model.
      values = {}
      normalizeby = {}
      # Iterate through all sparse features.
      for i in range(len(enroll_features)):
        feature = enroll_features[i]
        # Collect values by index.
        for j in range(feature.shape[1]):
          index = int(feature[0,j])
          value = feature[1,j]# / float(len(enroll_features))
          # Add values.
          if index in values:
            values[index] += value
            normalizeby[index] += 1
          else:
            values[index] = value
            normalizeby[index] = 1

      # Create model containing all the used indices.
      model = numpy.ndarray((2, len(values)), dtype = numpy.float64)

      i = 0
      for index in sorted(values.keys()):
        model[0,i] = index
        model[1,i] = values[index] / normalizeby[index]
        i+=1

    else:
      model = numpy.zeros(enroll_features[0].shape, dtype = numpy.float64)
      # All models.
      for i in range(len(enroll_features)):
        model += enroll_features[i]
      # Normalize by number of models.
      model /= float(len(enroll_features))

    # return enrolled model
    return model


  def inverted_index(self, model_ids, models):
    """Computes the Inverted Index File"""
    self.m_texts = {}
    self.m_kmeans_means = self.m_kmeans_machine.means.shape[0]
    words = set(word for word in range(self.m_kmeans_means))

    for i in range(len(model_ids)):
      self.m_texts[model_ids[i]] = models[i][0]

    # Form the inverted index
    self.m_invertedindex = {word:set(txt for txt, wrds in self.m_texts.items() if word in wrds) for word in words}


  def retrieval_method(self, probe):
    """Retrieves models according to the keywords from the Inverted Index File"""
    terms = probe[0]
    retrieved_list = reduce(set.intersection, (self.m_invertedindex[term] for term in terms), set(self.m_texts.keys()))
    return sorted(retrieved_list)


  def score(self, model, probe):
    """Computes the distance of the model to the probe using the distance function taken from the config file"""

    if self.m_sparse_histogram:
      return self.m_factor * self.m_distance_function(model[0,:], model[1,:], probe[0,:], probe[1,:])
    else:
      return self.m_factor * self.m_distance_function(model.flatten(), probe.flatten())
