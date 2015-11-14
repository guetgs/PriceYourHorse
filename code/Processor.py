import pandas as pd
import numpy as np
from collections import Counter
from kmeans_horses import Kmeans_DF


class Processor(object):
    '''
    Transforms horse information data into a format suitable for
    machine learning models.
    '''
    def __init__(self, sets, categories, fillna_method='mode'):
        '''
        INPUT: list of sets, list of strings, string
        OUTPUT: None

        Initializes internal variables.
        '''
        self.sets = sets
        for s in self.sets:
            if None in s:
                s.remove(None)
        self.categories = categories
        self.max_delta_h = 1
        self.max_age = 30
        self.centroids = None
        self.method = fillna_method
        
    def fit_transform(self, df, k=100):
        '''
        INPUT: pandas dataframe, int
        OUTPUT: pandas dataframe

        Fits internal variables used to fill missing values. Returns
        transformed data ready for machine learning models.
        '''
        if self.method == 'mode':
            self.fit_most_common_values(df)
        elif self.method == 'kmeans':
            self.max_age = max(df['Age'].values)
            self.max_delta_h = max(df['Height (hh)']) - min(df['Height (hh)'])
            print self.max_age, max(df['Height (hh)']), min(df['Height (hh)'])
            kmeans = Kmeans_DF(df, k, self.horse_horse_distance)
            self.centroids = kmeans.get_centroids()
            print 'centroids fitted...'
        return self.transform(df)

    def transform(self, df):
        '''
        INPUT: pandas dataframe
        OUTPUT: pandas dataframe

        Fills missing values in the data and converts categorical data
        to dummy variables.
        '''
        df = df.copy()
        # fillna for all rows
        df = self.fillna(df, method=self.method)

        # dummify
        for i, column in enumerate(self.categories):
            for cat in self.sets[i]:
                df[column + '_' + cat] = df[column].apply(lambda x: 1\
                                                          if x == cat\
                                                          else 0)
            df.drop(column, axis=1, inplace=True)
        return df
        

    def fit_most_common_values(self, df):
        '''
        INPUT: None
        OUPUT: None

        Determines and stores most common value for all columns.
        '''
        self.most_common_values = {}
        for column in df.columns:
            values = df[column].values
            values = [x for x in values if not pd.isnull(x)]
            if isinstance(values[0], (int, float)):
                most_common = np.array(values).mean()
            else:
                value_counts = Counter(values)
                most_common = value_counts.most_common(1)[0][0]
            self.most_common_values[column] = most_common

    def fillna(self, df, method='mode'):
        '''
        INPUT: pandas dataframe, string
        OUTPUT: pandas dataframe

        Fills missing values either using a dictionary of the most
        common values for categorical data or the mean value of
        numeric data, or using values of the most similar K-means
        centroid of the training data.
        '''
        if method == 'mode':
            columns = df.columns
            for col in columns:
                value = self.most_common_values[col]
                df[col].fillna(value, inplace=True)
        elif method == 'kmeans':
            for i, point in df.iterrows():
                if np.any(pd.isnull(point.values)):
                    dist = []
                    for j, cen in self.centroids.iterrows():
                        dist.append(self.horse_horse_distance(point, cent))
                    closest_cen = self.centroids.iloc[np.argmin(dist), :]
                    df.loc[i, :] = [x if not pd.isnull(x) else closest_cen[k]\
                                    for k, x in enumerate(point)]
        else:
            print 'error, no method selected for fillna'
        return df

    def horse_horse_distance(self, series1, series2):
        '''
        INPUT: pandas series, pandas series
        OUTPUT: float

        Calculates a distance measure based on equality of categorical
        data and normalized difference for numeric data.
        '''
        dist = 1
        N = 8.
        for col in ['Breed', 'Color', 'Pedigree', 'Sex']:
            if (pd.isnull(series1[col])) or (pd.isnull(series2[col])):
                N -= 1
            elif series1[col] != series2[col]:
                dist += 1
        if not (pd.isnull(series1['Height (hh)'])\
                or pd.isnull(series2['Height (hh)'])):
            dist += abs(series1['Height (hh)'] - series2['Height (hh)'])\
                    / self.max_delta_h
        else:
            N -= 1
        if not (pd.isnull(series1['Temperament'])\
                or pd.isnull(series2['Temperament'])):
            dist += abs(series1['Temperament'] - series2['Temperament'])
        else:
            N -= 1
        if not (pd.isnull(series1['Age']) or pd.isnull(series2['Age'])):
            dist += abs(series1['Age'] - series2['Age']) / self.max_age
        else:
            N -= 1
        return (dist / N - 1. / 8) * 8. / 7



