import numpy as np
from sklearn.ensemble import RandomForestRegressor
from scipy.stats import gaussian_kde
import seaborn as sns
import matplotlib.pyplot as plt

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

    def predictions(self, X):
        trees = self.model.estimators_
        preds = [tree.predict(X) for tree in trees]
        return np.array(preds)

    def predict_median(self, X):
        preds = self.predictions(X)
        return np.median(preds, axis=0)

    def predict_max_kde(self, X):
        preds = self.predictions(X)
        p = []
        for row in preds.T:
            fig = plt.figure()
            graph = sns.kdeplot(row.ravel(), shade=True, color='g', alpha=1)
            x,y = graph.get_lines()[0].get_data()
            ind = np.argmax(y)
            price = np.round(x[ind], decimals=-1)
            p.append(price)
            plt.close(fig)
            graph = None
        return p


    def score(self, X, y):
        return self.model.score(X, y)

    def cross_val_score(self):
        return self.model.oob_score_

    def feature_importance(self):
        importances = self.model.feature_importances_
        rank = np.argsort(importances)[::-1]
        return importances, rank

class RF_Predictor(RandomForestRegressor):
    
    def predictions(self, X):
        preds = [tree.predict(X) for tree in self.estimators_]
        return np.array(preds)

    def cross_val_score(self):
        return self.oob_score_

    def feature_importance(self):
        importances = self.feature_importances_
        rank = np.argsort(importances)[::-1]
        return importances, rank
