import flask
import pickle
import pandas as pd
from feature_lists import Skills, Temperaments, Breeds, Colors, Sexes

app = flask.Flask(__name__)

global PREPROCESSOR
global PREDICTOR

@app.route('/')
@app.route('/index')
def index():
    return flask.render_template('index.html')

@app.route('/submit')
def submit():
    return flask.render_template('form.html',\
                                 skills=Skills,\
                                 temperaments=Temperaments,\
                                 breeds=Breeds,\
                                 colors=Colors,\
                                 sexes=Sexes)

@app.route('/predictor', methods=['GET', 'POST'])
def prediction():
    global PREPROCESSOR
    global PREDICTOR
    if flask.request.method == 'GET':
        price = "Please tell something about your horse, first."
    else:
        print flask.request.form
        form = flask.request.form
        columns = ['Height (hh)', 'Weight (lbs)', 'Age', 'Temperament',\
                   'Sex', 'Breed', 'Color']
        data = {}
        data['_id'] = 1
        data['Pedigree'] = 1 if form['Pedigree'] == 'yes' else 0
        for col in columns:
            data[col] = form[col]
        data['Skills / Disciplines'] = []
        for key in form:
            print form[key]
            if form[key] == u'on':
                data['Skills / Disciplines'].append(key)
        data['Skills / Disciplines'] = str(data['Skills / Disciplines'])
        print data
        x = PREPROCESSOR.transform(data)
        price = PREDICTOR.predict(x)
        print x
        print price
        price = '${}'.format(price[0])
    return flask.render_template('prediction.html', price=price)
                                 

@app.route('/about_me')
def about_me():
    return flask.render_template('about_me.html')

@app.route('/details')
def details():
    return flask.render_template('details.html')

if __name__ == '__main__':
    global PREPROCESSOR
    global PREDICTOR
    with open('data/preprocessor.pickle', 'rb') as f:
        PREPROCESSOR = pickle.load(f)
    with open('data/predictor.pickle', 'rb') as f:
        PREDICTOR = pickle.load(f)
    print 'loaded...'
    app.run(host='0.0.0.0', port=8080, debug=True)
