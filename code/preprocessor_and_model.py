import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pickle
from preprocessor import BasicPreprocessor
from predictor import Predictor
from web_scraping import initiate_database

DB_NAME = 'horse_ads_database'
TABLE_NAME = 'horse_features_all'

MODEL_PARAMS = {'n_estimators': 100,
                'max_features': 'auto',
                'oob_score': True}

def load_all(table):
    df = pd.DataFrame([x for x in table.find()])
    return df

def get_X_y(df):
    complete_df = df[df['Price'] > 0]
    y = complete_df.Price.values
    complete_df = complete_df.drop(['Price', '_id'], axis=1)
    X = complete_df.values
    columns = list(complete_df.columns)
    return X, y, columns

def save_clean_df():
    table = initiate_database(DB_NAME, TABLE_NAME)
    df = load_all(table)
    preprocessor = BasicPreprocessor()
    clean_df = preprocessor.fit_transform(df)
    with open('../data/clean_df_all_pickle', 'wb') as f:
        pickle.dump(clean_df, f)

def plot_predicted_real(y, pred, title, show=True):
    plt.scatter(y, pred)
    plt.xlabel('Real Price [$]')
    plt.ylabel('Predicted Price [$]')
    plt.title(title)
    if show:
        plt.show()

if __name__ == '__main__':
    save_clean_df()
    with open('../data/clean_df_all_pickle', 'rb') as f:
        clean_df = pickle.load(f)
    X, y, features = get_X_y(clean_df)

    model = Predictor(MODEL_PARAMS)
    model.fit(X, y)
    print model.score(X, y)
    print model.cross_val_score()
    importances, rank = model.feature_importance()
    ranked_imp = zip(np.array(features)[rank], importances[rank])
    print ranked_imp[:20]

    pred = model.predict(X)
    plot_predicted_real(y, pred, 'RF model,100 trees, {:1.3f} oob_score'\
                        .format(model.cross_val_score()))
    

