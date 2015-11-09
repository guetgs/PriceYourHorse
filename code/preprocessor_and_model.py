import numpy as np
import pandas as pd
import pickle
from preprocessor import BasicPreprocessor
from web_scraping import initiate_database

DB_NAME = 'horse_ads_database'
TABLE_NAME = 'horse_features'

def load_all(table):
    df = pd.DataFrame([x for x in table.find()])
    return df

def get_X_y(df):
    complete_df = df[df['Price'] > 0]
    y = complete_df.Price.values
    complete_df.drop('Price', axis=1, inplace=True)
    X = complete_df.values
    return X, y

if __name__ == '__main__':
    table = initiate_database(DB_NAME, TABLE_NAME)
    df = load_all(table)
    preprocessor = BasicPreprocessor()
    clean_df = preprocessor.fit_transform(df)
    with open('../data/clean_df_pickle', 'wb') as f:
        pickle.dump(clean_df, f)
    X, y = get_X_y(clean_df)