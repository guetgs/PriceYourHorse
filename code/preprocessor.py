import numpy as np
import pandas as pd
import datetime
from collections import Counter


class BasicPreprocessor(object):

    def __init__(self):
        '''
        INPUT: None
        OUTPUT: None

        Initializes attributes
        '''
        self.df = None
        self.final_columns = None
        self.most_common_values = None

    def fit_transform(self, df):
        '''
        INPUT: dataframe
        OUTPUT: dataframe

        Performs all processing steps from raw data to data that can be used
        to fit a model.
        '''
        self.df = df.copy()
        self.clean_up()
        self.fit_most_common_values()
        self.fillna()
        self.engineer_features()
        return self.select_features()

    def clean_up(self):
        '''
        INPUT: None
        OUTPUT: None

        Cleans data in internal dataframe into consistent
        format and datatype.
        '''
        df = self.df
        df.drop_duplicates(['Breed', 'Color', 'Foal Date', 'Height (hh)',
                            'In Foal', 'Markings', 'Name', 'Sex',
                            'State Bred', 'Temperament', 'Weight (lbs)',
                            'City', 'Pedigree', 'Price', 'State'],
                            inplace=True)
        
        # Create Dummy Variables for all Skills/Disciplines
        # present in the data set.
        df['Skills / Disciplines'] = df['Skills / Disciplines'].fillna(u'-')
        df['Skills / Disciplines'] = df['Skills / Disciplines']\
                                     .apply(lambda y: [] if y == u'-'
                                            else y.split(', '))
        skills = Counter([x for y in df['Skills / Disciplines'] for x in y])
        for skill, val in skills.iteritems():
            if val > 10:
                df[skill] = df['Skills / Disciplines'].apply(lambda x: 1\
                                                             if skill in x\
                                                             else 0)
        df.drop('Skills / Disciplines', axis=1, inplace=True)
        # Replace missing values '-' by None
        df = df.apply(lambda x: x.apply(lambda y: None if y == u'-' else y))
        
        # Apply individual clean up functions to columns
        df['Price'] = df['Price'].apply(self.clean_price)
        df['Ad Created'] = df['Ad Created'].apply(self.clean_date)
        df['Foal Date'] = df['Foal Date'].apply(self.clean_date)
        df['Last Update'] = df['Last Update'].apply(self.clean_date)
        df['Height (hh)'] = df['Height (hh)'].apply(self.clean_height)
        df['Temperament'] = df['Temperament'].apply(lambda x: eval(x + '.')\
                                                    if isinstance(x, unicode)\
                                                     else None)
        df['Weight (lbs)'] = df['Weight (lbs)'].astype('float')\
                                               .apply(lambda x: None\
                                                      if x > 3000 else abs(x))
        self.df = df

    def clean_price(self, s):
        '''
        INPUT: string
        OUTPUT: float or None

        Converts string containing price into float. Converts Euro into dollar
        using an exchange rate of 1.1. Returns None if s does not start with
        either u'$' or unicode for Euro.
        '''
        if isinstance(s, unicode):
            if s[0] == u'\u20ac':
                return float(s[1:].replace(',', '')) * 1.1
            if s[0] == u'$':
                x = s.replace(',', '').split(' ')[0]
                return float(x[1:])
        return None
    
    def clean_date(self, s):
        '''
        INPUT: string
        OUPUT: pandas datetime

        Converts s to datetime. If automatic conversion fails, asks user to
        correct the date. Accepts 'None' if date cannot be reasonably
        corrected.
        '''
        try:
            date = pd.to_datetime(s, errors='raise')
        except:
            date = s
        while isinstance(date, unicode):
            d = raw_input('Please correct this date: {} '.format(date))
            if d == 'None':
                date = None
            else:
                date = pd.to_datetime(d)
        return date

    def clean_height(self, h):
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

    def fit_most_common_values(self):
        '''
        INPUT: None
        OUPUT: None

        Determines and stores most common value for all columns except Price,
        since Price is the prediction target.
        '''
        self.most_common_values = {}
        for column in self.df.columns:
            values = self.df[column].values
            values = [x for x in values if not pd.isnull(x)]
            value_counts = Counter(values)
            most_common = value_counts.most_common(1)[0][0]
            self.most_common_values[column] = most_common

    def fillna(self):
        '''
        INPUT: None
        OUTPUT: None

        Fills missing values with most common value for each column.
        '''
        columns = list(self.df.columns.values)
        columns.remove(u'Price')
        for column in columns:
            value = self.most_common_values[column]
            self.df[column].fillna(value, inplace=True)

    
    def engineer_features(self):
        '''
        INPUT: None
        OUTPUT: None

        Engineers new features and dummifies selected categorical features.
        '''
        self.df['Age'] = self.df['Foal Date'].apply(self.add_age)
        self.dummify(['Breed', 'Color', 'Sex'])
        

    def add_age(self, foal_date):
        '''
        INPUT: datetime
        OUPUT: float

        Determines horse age from foal date.
        '''
        age = datetime.date.today().year - foal_date.year
        mode_foal_date = self.most_common_values['Foal Date']
        mode_foal_date = pd.to_datetime(mode_foal_date)
        mode_age = datetime.date.today().year - mode_foal_date.year
        if (age < 0) or (age > 40):
            age = mode_age
        return age

    def dummify(self, columns):
        '''
        INPUT: list of strings
        OUTPUT: None

        Creates dummy variables for all categories present the columns
        defined by the input parameter.
        '''
        self.df = pd.get_dummies(self.df, columns=columns)


    def select_features(self):
        '''
        INPUT: None
        OUTPUT: dataframe

        Selects columns to serve as features for a regression model.
        '''
        columns = list(self.df.columns.values)
        rm = [u'Foal Date', u'In Foal', u'Markings', u'Name', u'State Bred',
              u'City', u'State', u'Ad Created', u'Last Update', u'Description',
              u'Registry Number', u'Registry', u'Ad Number']
        for column in rm:
            columns.remove(column)
        self.final_columns = columns
        return self.df[self.final_columns]

    def transform(self, df):
        '''
        INPUT: dataframe
        OUTPUT: dataframe

        Transforms input dataframe to meet the format required to serve as
        input data into a model.
        '''


