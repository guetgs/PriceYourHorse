# PriceYourHorse
Project in the context of Galvanize Data Science Immersive Program

### Description
PriceYourHorse is a web application that predicts the price of a horse based on features and keywords selected by the user. In addition to the final prediction, it shows how the individual estimators of the underlying model are distributed.

### Elements
The [Web_App](https://github.com/guetgs/PriceYourHorse/tree/master/Web_App) folder contains the web application, which is written in python2 and based on [Flask](http://flask.pocoo.org/). Its subfolders contain the trained predictive elements, all html templates and the [Bootstrap](http://getbootstrap.com/) css stylesheets and images. The application imports some of the modules present in the [code](https://github.com/guetgs/PriceYourHorse/tree/master/code) folder, and relies on predictive elements that could not be included here due to size constraints. These elements are generated using additional code provided in the [code](https://github.com/guetgs/PriceYourHorse/tree/master/code) folder.

The [LogBook](https://github.com/guetgs/PriceYourHorse/tree/master/LogBook) shows records of individual steps during feature engineering and model development with respect to their influence on preditive performance.

Project Proposal and Timeline were used to guide developing the application and ensured timely completion of the project.

### Libraries
Python libraries required to run this application are collections, flask, matplotlib, nltk, numpy, pandas, pickle, seaborn, sklearn, string, StringIO and urllib.
Code used to develop the application is also dependent on bs4 (BeautifulSoup), csv, datetime, os, pymongo, requests and threading. Furthermore, [MongoDB](https://www.mongodb.org/) was used during development.