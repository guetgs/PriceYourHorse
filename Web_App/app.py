import flask
import pickle
import pandas as pd

app = flask.Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return flask.render_template('index.html')

@app.route('/submit')
def submit():
    return flask.render_template('form.html')

@app.route('/predictor', methods=['GET', 'POST'])
def prediction():
    price = '$1000'
    return flask.render_template('prediction.html', price=price)

@app.route('/about_me')
def about_me():
    return flask.render_template('about_me.html')

@app.route('/details')
def details():
    return flask.render_template('details.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)