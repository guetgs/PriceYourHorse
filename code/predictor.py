import numpy as np
from sklearn.ensemble import RandomForestRegressor

class Predictor(object):

    def __init__(self, params):
        self.model = RandomForestRegressor(**params)

    def fit(self, X, y):
        return self.model.fit(X, y)

    def fit_transform(self, X, y):
        return self.model.fit_transform(X, y)

    def transform(self, X):
        return self.model.transform(X)

    def predict(self, X):
        return self.model.predict(X)

    def score(self, X, y):
        return self.model.score(X, y)

    def cross_val_score(self):
        return self.model.oob_score_

    def feature_importance(self):
        importances = self.model.feature_importances_
        rank = np.argsort(importances)[::-1]
        return importances, rank
