import flask
import pickle
import sys
import urllib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from StringIO import StringIO
sys.path.append('../code/')
from feature_lists import Vocab, Temperaments
from feature_dict import Breeds_dict, Color_dict, Sex_dict
from tokenizer import tokenizer


app = flask.Flask(__name__)

global PROCESSOR
global PREDICTOR
global VECTORIZER
with open('data/vectorizer.pickle', 'rb') as f:
    VECTORIZER = pickle.load(f)
with open('data/processor.pickle', 'rb') as f:
    PROCESSOR = pickle.load(f)
with open('data/predictor.pickle', 'rb') as f:
    PREDICTOR = pickle.load(f)
print('loaded...')


@app.route('/')
@app.route('/index')
def index():
    '''
    INPUT: None
    OUTPUT: html page

    Returns static html start page.
    '''
    return flask.render_template('index.html')


@app.route('/submit')
def submit():
    '''
    INPUT: None
    OUTPUT: html page

    Prepares variable selection for user input form and returns
    user input form html page.
    '''
    dicts = [Breeds_dict,
             Color_dict,
             Sex_dict]
    key_list = [d.keys() for d in dicts]
    for i, l in enumerate(key_list):
        key_list[i] = [x for x in l
                       if x not in [u'-', None, np.nan, 'Unknown']]
        key_list[i].sort()
    Vocab.sort()
    return flask.render_template('form.html',
                                 skills=Vocab,
                                 temperaments=Temperaments,
                                 breeds=key_list[0],
                                 colors=key_list[1],
                                 sexes=key_list[2])


@app.route('/about_me')
def about_me():
    '''
    INPUT: None
    OUTPUT: html page

    Returns static html author description page.
    '''
    return flask.render_template('about_me.html')


@app.route('/details')
def details():
    '''
    INPUT: None
    OUTPUT: html page

    Returns static html app description page.
    '''
    return flask.render_template('details.html')


@app.route('/predictor', methods=['GET', 'POST'])
def prediction():
    '''
    INPUT: None
    OUTPUT: html page

    Reformats user input and provides a price estimation and a plot
    showing the prediction distribution of individual estimators.
    '''
    global PREPROCESSOR
    global PREDICTOR
    global VECTORIZER
    if flask.request.method == 'GET':
        return flask.render_template('prediction_noinput.html')
    else:
        df = prepare_dataframe(flask.request.form)
        X_text = VECTORIZER.transform(df['Description'])

        df_X = df.drop('Description', axis=1)
        df_X_tabular = PROCESSOR.transform(df_X)

        X = np.hstack((df_X_tabular.values, X_text.todense()))

        price = np.round(PREDICTOR.predict(X)[0], decimals=-2)
        price_string = '${}'.format(int(price))
        img = prepare_graph(PREDICTOR.predictions(X), price)
        data = img.getvalue().encode('base64')
        image_url = 'data:image/png;base64,{}'\
                    .format(urllib.quote(data.rstrip('\n')))
        return flask.render_template('prediction.html', price=price_string,
                                     image_url=image_url)


def prepare_graph(preds, price):
    '''
    INPUT: 1D array, float
    OUTPUT: StringIO object containing a png image

    Provides a KDE plot of the distribution of individual estimates
    with a line indicating the predicted price and a 5 to 95 percentile
    range.
    '''
    perc_5 = np.percentile(preds, 5)
    perc_95 = np.percentile(preds, 95)
    plt.figure()
    plt.axvspan(perc_5, perc_95, color='k', alpha=0.3)
    graph = sns.kdeplot(preds.ravel(), shade=True, color='g', alpha=1)
    y_max = plt.ylim()[1]
    plt.axvline(price, ymax=0.89, color='k', alpha=1)
    plt.annotate('Prediction', xy=(price, 0.8 * y_max),
                 xytext=(price + 3000, 0.82 * y_max), color='k',
                 arrowprops={'arrowstyle': '->',
                             'facecolor': 'black',
                             'alpha': 1,
                             'color': 'k',
                             'linestyle': 'solid',
                             'linewidth': 1})
    plt.annotate('5 - 95 Percentile',
                 xy=((perc_95 + perc_5) / 2, 0.93*y_max),
                 ha='center', color='k')
    plt.annotate('', xy=(perc_5, 0.91 * y_max),
                 xytext=(perc_95, 0.91 * y_max), color='k',
                 arrowprops={'arrowstyle': '<->',
                             'facecolor': 'black',
                             'alpha': 1,
                             'color': 'k',
                             'linestyle': 'solid',
                             'linewidth': 1})
    plt.title('Predictions of Individual Estimators',
              fontsize=20, weight='bold')
    plt.xlabel('Price [$]', fontsize=18)
    plt.ylabel('Kernel Density Estimate', fontsize=18)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.tight_layout()
    image = StringIO()
    sns.plt.savefig(image, format='png')
    return image


def prepare_dataframe(form):
    '''
    INPUT: flask request form
    OUTPUT: pandas dataframe

    Converts user input from request form into dataframe. Performs
    some preprocessing of the data to meet the format required for
    processing and vectorizing.
    '''
    columns = ['Height (hh)', 'Age', 'Temperament',
               'Sex', 'Breed', 'Color']
    data = {}
    data['Pedigree'] = 1 if form['Pedigree'] == 'yes' else 0
    for col in columns:
        data[col] = form[col]
    data['Temperament'] = eval(data['Temperament'] + '.')
    if data['Height (hh)']:
        data['Height (hh)'] = float(data['Height (hh)'])
    else:
        data['Height (hh)'] = None
    if data['Age']:
        data['Age'] = int(data['Age'])
    else:
        data['Age'] = None
    data['Description'] = []
    for key in form:
        if form[key] == u'on':
            data['Description'].append(key)
    data['Description'] = ', '.join([x for x in data['Description']])
    return pd.Series(data).to_frame().transpose()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
