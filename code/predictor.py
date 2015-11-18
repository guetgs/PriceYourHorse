import numpy as np
from sklearn.ensemble import RandomForestRegressor


class RF_Predictor(RandomForestRegressor):
    '''
    Predictor derived from RandomForestRegressor with additional
    analytical methods.
    '''
    def predictions(self, X):
        '''
        INPUT: 2D numpy array
        OUTPUT: 2D numpy array

        Returns predictions of individual estimators of the forest.
        Output matrix is N_trees x N_samples.
        '''
        preds = [tree.predict(X) for tree in self.estimators_]
        return np.array(preds)

    def cross_val_score(self):
        '''
        INPUT: None
        OUTPUT: float

        Returns out of bag score of the training data.
        '''
        return self.oob_score_

    def feature_importance(self):
        '''
        INPUT: None
        OUTPUT: 1D array, 1D array

        Returns feature importance scores and their ranking.
        '''
        importances = self.feature_importances_
        rank = np.argsort(importances)[::-1]
        return importances, rank
