import numpy as np
import pandas as pd
from collections import Counter

from timeit import default_timer as timer

class Kmeans_DF(object):
    '''
    K-means classifier working on pandas dataframes.
    '''
    def __init__(self, df, k, dist_func):
        '''
        INPUT: pandas dataframe, int, function
        OUTPUT: None

        Initialized internal variables. Accepts data as a
        dataframe, sets the number of centroids to k and uses the provided
        function to calculate distances between points.
        '''
        self.k = k
        self.centroids = None
        self.points = df
        self.distances = None
        self.n_points = df.shape[0]
        self.assignments = np.zeros((self.n_points, 1), dtype=int)
        self.max_iter = 1000
        self.done = False
        self.current_dist = np.zeros((self.n_points, 1), dtype=float)
        self.dist_func = dist_func

    def init_centroids(self):
        '''
        INPUT: None
        OUTPUT: None

        Initializes centroids to random points in the dataset.
        '''
        inds = np.random.choice(range(0, self.n_points), size=self.k, replace=False)
        self.centroids = self.points.iloc[inds, :]

    def get_distances(self):
        '''
        INPUT: None
        OUTPUT: None

        Calculates distances of each point to each centroid.
        '''
        self.distances = []
        for i, point in self.points.iterrows():
            dist = [self.dist_func(point, x[1]) for x in self.centroids.iterrows()]
            self.distances.append(dist)

    def assign_points(self):
        '''
        INPUT: None
        OUTPUT: None

        Assigns points to the closest centroid. Sets flag if none
        of the assignments change.
        '''
        assignment = self.assignments.copy()
        for i, dist in enumerate(self.distances):
            ind = np.argmin(dist)
            self.assignments[i] = ind
            self.current_dist[i] = np.array(dist)[ind]
        if np.all(assignment == self.assignments):
            self.done = True

    def move_centroids(self):
        '''
        INPUT: None
        OUTPUT: None

        Moves centroids based on the assigned points.
        '''
        for cen in xrange(self.k):
            ind = (self.assignments == cen)[:, 0]
            points = self.points.iloc[ind, :]
            self.centroids.iloc[cen, :] = self.calc_centroid(points)

    def calc_centroid(self, points):
        '''
        INPUT: pandas dataframe
        OUTPUT: pandas series

        Calculates centroid of the points in the dataframe. Uses mode for
        categorical values and mean for numeric values. Excludes Null-type
        values unless there are no other values present.
        '''
        most_common_values = {}
        for column in points.columns:
            values = points[column].values
            values = [x for x in values if not pd.isnull(x)]
            if values:
                if isinstance(values[0], (int, float)):
                    most_common = np.array(values).mean()
                else:
                    value_counts = Counter(values)
                    most_common = value_counts.most_common(1)[0][0]
            else:
                most_common = None
            most_common_values[column] = most_common
        return pd.Series(most_common_values)


    def get_centroids(self):
        '''
        INPUT: None
        OUTPUT: pandas dataframe

        Iterates over getting the point-centroid distances and assigning
        points to centroids until convergence or the maximum interations
        are reached. Returns centroids.
        '''
        self.init_centroids()
        it = 0
        while it < self.max_iter:
            self.get_distances()
            self.assign_points()
            if self.done == True:
                break
            self.move_centroids()
            it += 1
            if np.mod(it, 5) == 0:
                print '{} iterations done ...'.format(it)
        return self.centroids

    def get_clusters(self):
        '''
        INPUT: None
        OUTPUT: list

        Iterates over getting the point-centroid distances and assigning
        points to centroids until convergence or the maximum interations
        are reached. Returns list of cluster assignments.
        '''
        self.init_centroids()
        it = 0
        while it < self.max_iter:
            self.get_distances()
            self.assign_points()
            if self.done == True:
                break
            self.move_centroids()
            it += 1
            if np.mod(it, 5) == 0:
                print '{} iterations done ...'.format(it)
        return self.assignments.reshape(1, len(self.assignments))[0]






