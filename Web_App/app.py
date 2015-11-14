import flask
import pickle
import sys
import pandas as pd
import numpy as np
sys.path.append('../code/')
sys.path.append('../code_temp/')
from feature_lists import Skills, Temperaments, Breeds, Colors, Sexes, Vocab
from preprocessor_and_model_temp import tokenizer


app = flask.Flask(__name__)

global PREPROCESSOR
global PREDICTOR
global VECTORIZER

@app.route('/')
@app.route('/index')
def index():
    return flask.render_template('index.html')

@app.route('/submit')
def submit():
    Vocab.sort()
    print Vocab
    return flask.render_template('form.html',\
                                 skills=Vocab,\
                                 temperaments=Temperaments,\
                                 breeds=Breeds,\
                                 colors=Colors,\
                                 sexes=Sexes)

@app.route('/about_me')
def about_me():
    return flask.render_template('about_me.html')

@app.route('/details')
def details():
    return flask.render_template('details.html')

@app.route('/predictor', methods=['GET', 'POST'])
def prediction():
    global PREPROCESSOR
    global PREDICTOR
    global VECTORIZER
    if flask.request.method == 'GET':
        flask.render_template('prediction_noinput.html')
    else:
        print flask.request.form
        df = prepare_dataframe(flask.request.form)
        print df
        X_text = VECTORIZER.transform(df['Description'])
        print 'shape X_text: ', X_text.todense()

        df_X = df.drop('Description', axis=1)
        df_X_tabular = PROCESSOR.transform(df_X)
        print 'shape df_X_tabular: ', df_X_tabular.values
        
        X = np.hstack((df_X_tabular.values, X_text.todense()))

        price = PREDICTOR.predict(X)
        print X
        print price
        price = '${}'.format(price[0])
    return flask.render_template('prediction.html', price=price)

def prepare_dataframe(form):
    columns = ['Height (hh)', 'Age', 'Temperament',\
               'Sex', 'Breed', 'Color']
    data = {}
    data['Pedigree'] = 1 if form['Pedigree'] == 'yes' else 0
    for col in columns:
        data[col] = form[col]
    data['Temperament'] = eval(data['Temperament'] + '.')
    data['Height (hh)'] = float(data['Height (hh)'])
    data['Age'] = int(data['Age'])


    data['Description'] = []
    for key in form:
        print form[key]
        if form[key] == u'on':
            data['Description'].append(key)
    data['Description'] = ', '.join([x for x in data['Description']])
    print data
    return pd.Series(data).to_frame().transpose()
                                 

if __name__ == '__main__':
    global PROCESSOR
    global PREDICTOR
    global VECTORIZER
    with open('data/vectorizer.pickle', 'rb') as f:
        VECTORIZER = pickle.load(f)
    with open('data/processor.pickle', 'rb') as f:
        PROCESSOR = pickle.load(f)
    with open('data/predictor.pickle', 'rb') as f:
        PREDICTOR = pickle.load(f)
    print 'loaded...'
    app.run(host='0.0.0.0', port=8080, debug=True)

