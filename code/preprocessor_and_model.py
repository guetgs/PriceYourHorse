import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pickle
import statsmodels.api as sm
from preprocessor import BasicPreprocessor
from predictor import Predictor
from web_scraping import initiate_database

DB_NAME = 'horse_ads_database'
TABLE_NAME = 'horse_features_all'

MODEL_PARAMS = {'n_estimators': 100,
                'max_features': 'auto',
                'oob_score': True,
                'n_jobs': -1}

def load_all(table):
    df = pd.DataFrame([x for x in table.find()])
    return df

def identify_y_outlier_borders(y):
    y_working = y[y > 0]
    mean = y_working.mean()
    std = y_working.std()
    return 3 * std


def get_X_y(df):
    upper_border = 60000
    complete_df = df[(df['Price'] > 0) & (df['Price'] < upper_border)]
    y = complete_df.Price.values
    complete_df = complete_df.drop(['Price', '_id'], axis=1)
    X = complete_df.values
    columns = list(complete_df.columns)
    return X, y, columns

if __name__ == '__main__':
    table = initiate_database(DB_NAME, TABLE_NAME)
    df = load_all(table)
    df.drop_duplicates(['Breed', 'Color', 'Foal Date', 'Height (hh)',
                                'In Foal', 'Markings', 'Name', 'Sex',
                                'State Bred', 'Temperament', 'Weight (lbs)',
                                'City', 'Pedigree', 'State'],
                                inplace=True)
    df = df.reset_index().drop('index', axis=1)
    df_X = df.drop('Price', axis=1)
    preprocessor = BasicPreprocessor()
    clean_df = preprocessor.fit_transform(df_X)
    clean_df['Price'] = preprocessor.clean_prices(df['Price'])
    X, y, features = get_X_y(clean_df)
    print X.shape, y.shape
    model = Predictor(MODEL_PARAMS)
    model.fit(X, y)
    with open('../Web_App/data/preprocessor.pickle', 'wb') as f:
        pickle.dump(preprocessor, f)
    with open('../Web_App/data/predictor.pickle', 'wb') as f:
        pickle.dump(model, f)
   