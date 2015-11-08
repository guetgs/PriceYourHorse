import numpy as np
import pandas as pd
import datetime
import re
import pickle
from pymongo import MongoClient
from collections import Counter


class BasicPreprocessor(object):

	def __init__(self):
		self.df = None

	def fit_transform(self, df):
		self.df = df.copy()
		self.clean_up()
		self.engineer_features()
		self.fillna()
		return self.select_features()

	def clean_up(self):
		'''
		INPUT: None
		OUTPUT: None

		Cleans data in internal dataframe into consistent
		format and datatype.
		'''
		pass

	def engineer_features(self):
		pass