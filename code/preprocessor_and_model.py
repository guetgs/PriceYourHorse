import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import datetime
import string
import csv
from pymongo import MongoClient
from Processor import Processor
from feature_dict import Breeds_dict, Color_dict, Sex_dict
from feature_lists import Vocab, Vocab_snowball
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer
from predictor import Predictor

DB_NAME = 'horse_ads_database'
TABLE_NAME = 'horse_features_all'

PRICE_RANGE = [150, 60000]

FILLNA_METHOD = 'mode'
N_CENTROIDS = 100

CATEGORIES = ['Breed', 'Color', 'Sex']

MODEL_PARAMS = {'n_estimators': 100,
                'max_features': 'sqrt',
                'oob_score': True,
                'n_jobs': -1}


def plot_predicted_real(y, pred, title, show=True):
    plt.scatter(y, pred)
    plt.xlabel('Real Price [$]')
    plt.ylabel('Predicted Price [$]')
    plt.title(title)
    if show:
        plt.show()

def initiate_database(db_name, table_name):
    '''
    INPUT: string, string
    OUTPUT: mongodb table

    Connects to mongodb database db_name and table table_name through
    pymongo and returns handle to table.
    '''
    client = MongoClient()
    db = client[db_name]
    table = db[table_name]
    return table


def load_all(table, price=True):
    '''
    INPUT: mongodb table, boolean
    OUTPUT pandas dataframe

    Depending on the price flag, loads all data or only data containing
    a price from the mongodb table into a DataFrame.
    '''
    if price:
        df = pd.DataFrame([x for x in table.find({'Price': {'$exists': True}})])
    else:
        df = pd.DataFrame([x for x in table.find()])
    return df


def preprocess_dataframe(df):
    '''
    INPUT: pandas dataframe
    OUTPUT: pandas dataframe

    Preprocesses data into a format accepted by the Processor. This involves
    dropping, merging or adding columns, changing variable types, cleaning
    data and reducing categories for categorical data.
    '''
    df.drop_duplicates(['Breed', 'Color', 'Foal Date', 'Height (hh)',
                        'In Foal', 'Markings', 'Name', 'Sex',
                        'State Bred', 'Temperament', 'Weight (lbs)',
                        'City', 'Pedigree', 'State'],
                        inplace=True)
    df['Description'] = df['Description'] + df['Skills / Disciplines']
    df['Description'] = df['Description']\
                        .apply(lambda x: '' if x == u'-' else x)
    df = df.apply(lambda x: x.apply(lambda y: None if y == u'-' else y))
    df['Foal Date'] = df['Foal Date'].apply(clean_date)
    df['Age'] = df['Foal Date'].apply(add_age)
    df.drop([u'In Foal', u'Markings', u'Name', u'State Bred',
             u'Skills / Disciplines', u'Foal Date', u'_id',
             u'City', u'State', u'Ad Created', u'Last Update',
             u'Registry Number', u'Registry', u'Ad Number', u'Weight (lbs)'],
             axis=1, inplace=True)
    df['Temperament'] = df['Temperament']\
                        .apply(lambda s: eval(s + '.')\
                               if isinstance(s, unicode) else None)
    df['Height (hh)'] = df['Height (hh)'].apply(clean_height)

    # dicts = [Breeds_dict, Color_dict, Sex_dict]
    # for i, cat in enumerate(CATEGORIES):
    #     df[cat] = df[cat].apply(lambda x: dicts[i][x] if not pd.isnull(x) else x)

    df['Price'] = df['Price'].apply(clean_price)
    return df


def fit_processor(df_X):
    '''
    INPUT: pandas dataframe
    OUTPUT: pandas dataframe

    Fits Processor and transforms data into numeric formats suitable for
    feeding into a model. Saves fitted Processor for further use in
    web application.
    '''
    dicts = [Breeds_dict,
             Color_dict,
             Sex_dict]
    p = Processor(dicts, CATEGORIES, FILLNA_METHOD)
    df_X_tabular = p.fit_transform(df_X, N_CENTROIDS)
    with open('../Web_App/data/processor.pickle', 'wb') as f:
        pickle.dump(p, f)
    return df_X_tabular

def fit_vectorizer(descriptions):
    '''
    INPUT: list of strings or pandas series of strings
    OUTPUT: pandas dataframe

    Fits TfidfVectorizer and transforms strings into word feature matrix.
    Returns dataframe of the feature matrix with feature names as column
    names.
    '''
    vec = TfidfVectorizer(strip_accents='unicode',\
                          stop_words='english',\
                          ngram_range=(1, 1),\
                          min_df=100,\
                          tokenizer=tokenizer,\
                          vocabulary=Vocab,\
                          use_idf=True)
    X_text = vec.fit_transform(descriptions)
    feature_names = ['Skill_' + name for name in vec.get_feature_names()]
    df_X_text = pd.DataFrame(X_text.todense(), columns=feature_names)
    with open('../Web_App/data/vectorizer.pickle', 'wb') as f:
        pickle.dump(vec, f)
    return df_X_text
    


def clean_price(s):
    '''
    INPUT: string
    OUTPUT: float or None

    Converts string containing price into float. Converts Euro into dollar
    using an exchange rate of 1.1. Returns None if s does not start with
    either u'$' or unicode for Euro.
    '''
    if s[0] == u'\u20ac':
        return float(s[1:].replace(',', '')) * 1.1
    if s[0] == u'$':
        x = s.replace(',', '').split(' ')[0]
        return float(x[1:])
    else:
        print 'error', s
        return -1.


def clean_date(s):
    '''
    INPUT: string
    OUTPUT: pandas datetime

    Converts s to datetime. If automatic conversion fails, asks user to
    correct the date. Accepts 'None' if date cannot be reasonably
    corrected.
    '''
    try:
        date = pd.to_datetime(s, errors='raise')
    except:
        date = s
    while isinstance(date, unicode):
        if date == u'-':
            return None
        d = raw_input('Please correct this date: {} '.format(date))
        if d == 'None':
            date = None
        else:
            date = pd.to_datetime(d)
    return date


def clean_height(h):
    '''
    INPUT: string
    OUTPUT: float

    Transforms hight from string to float. If the value is unrealistically
    high for a horse, the hight is set to None. If the value appears to
    be in inches instead of hands, it is converted into hands.
    '''
    if isinstance(h, unicode):
        h = abs(float(h))
        if h > 90:
            return None
        if h > 22:
            return h * 2.54 / 10.16
        return h
    return None


def add_age(foal_date):
    '''
    INPUT: datetime
    OUTPUT: float

    Determines horse age from foal date.
    '''
    if foal_date:
        age = datetime.date.today().year - foal_date.year
        if (age < 0) or (age > 40):
            age = None
        return age
    else:
        return None


def tokenizer(s):
    '''
    INPUT: string
    OUTPUT: list of strings

    Tokenizes string into list of words.
    '''
    token = word_tokenize(s.lower())
    stpw = set(stopwords.words('english'))
    exclude = set(string.punctuation)
    clean = [w for w in token if w not in stpw and w not in exclude]
    wordnet = WordNetLemmatizer()
    lemmatized = [wordnet.lemmatize(word) for word in clean]
    snowball = SnowballStemmer('english')
    stemmed = [snowball.stem(word) for word in clean]
    return lemmatized

def feature_importance_analysis(features, model):
    importances, rank = model.feature_importance()
    ranked_imp = zip(np.array(features)[rank], importances[rank])
    print ranked_imp[:50]
    vocabulary = [w for w in np.array(features)[rank] if w[:6] == 'Skill_']
    with open('vocab.csv', 'w') as f:
        wr = csv.writer(f, delimiter=',')
        wr.writerow(vocabulary[:200])


if __name__ == '__main__':
    table = initiate_database(DB_NAME, TABLE_NAME)
    df = load_all(table, price=True)
    print 'dataframe loaded...'
    df = preprocess_dataframe(df)
    print 'dataframe preprocessed...'
    df = df[(df['Price'] > PRICE_RANGE[0]) & (df['Price'] < PRICE_RANGE[1])]
    df = df.reset_index().drop('index', axis=1)

    # separate target, tabular features, text features
    y = df['Price'].values
    descriptions = df['Description']
    df_X = df.drop(['Price', 'Description'], axis=1)
    df_X.to_json('Processor_input_dataframe.json')
    # process tabular features
    df_X_tabular = fit_processor(df_X)
    print 'tabular features processed...'
    # process text features
    df_X_text = fit_vectorizer(descriptions)
    print 'text features processed...'
    
    df_X_final = pd.concat([df_X_tabular, df_X_text], axis=1)
    features = df_X_final.columns
    X = df_X_final.values
    with open('X.pickle', 'wb') as f:
        pickle.dump(X, f)
    with open('y.pickle', 'wb') as f:
        pickle.dump(y, f)

    model = Predictor(MODEL_PARAMS)
    model.fit(X, y)
    with open('../Web_App/data/predictor.pickle', 'wb') as f:
        pickle.dump(model, f)
    print model.score(X, y)
    print model.cross_val_score()
    pred = model.predict(X)
    plot_predicted_real(y, pred, 'RF model,100 trees, {:1.3f} oob_score'\
                        .format(model.cross_val_score()))











