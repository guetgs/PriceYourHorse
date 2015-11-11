import numpy as np
import pandas as pd
import datetime
from feature_dict import Color_dict, Breeds_dict
from collections import Counter

SKILLS = ['Incentive Fund', 'Register Of Merit', 'Companion',\
          'English Pleasure', 'Color Producer', 'Import', 'Homozygous Grey',\
          'Show Experience', 'Endurance', 'All Around', 'Parade',\
          'Racehorse', 'Finished', 'Field Hunter', 'Trick', 'Equitation',\
          'Driving', 'Started Under Saddle', 'Dressage', 'Show Winner',\
          'Trail', 'Athletic', 'Longe Line', 'Reining', 'Project',\
          'Trail Riding', 'Racing', 'Show Hack', 'Breeding', 'Pony Club']

BREEDS = ['Akhal Teke', 'Andalusian', 'Appaloosa', 'Arabian', 'Barb',\
          'Bashkir Curly', 'Belgian', 'Canadian', 'Chincoteague Pony',\
          'Connemara Pony', 'Crossbred Pony', 'Dales Pony', 'Dartmoor Pony',\
          'Donkey', 'Dutch', 'Exmoor Pony', 'Fjord', 'Highland Pony',\
          'Florida Cracker', 'Friesian', 'Gotland Pony', 'Hackney',\
          'Haflinger', 'Half Arabian', 'Hanoverian', 'Heavy Horse',\
          'Holsteiner', 'Hungarian', 'Iberian', 'Icelandic', 'Irish Draught',\
          'Knabstrupper', 'Lipizzan', 'Marchador', 'Miniature',\
          'Missouri Fox Trotter', 'Morab', 'Morgan', 'Mule', 'Mustang',\
          'New Forest Pony', 'Newfoundland Pony', 'Nokota', 'Oldenburg',\
          'Paint', 'Paint Pony', 'Palomino', 'Paso Fino', 'Pinto',\
          'Pony', 'Quarter Horse', 'Saddlebred', 'Shetland Pony', 'Shire',\
          'Standardbred', 'Tennessee Walking', 'Thoroughbred', 'Tiger',\
          'Trakehner', 'Walkaloosa', 'Warmblood', 'Welsh Cob', 'Welsh Pony',\
          'Westphalian', 'Other']

COLORS = ['Bay', 'Black', 'Brindle', 'Brown', 'Buckskin', 'Champagne',\
          'Chestnut', 'Chocolate', 'Cremello', 'Dun', 'Grey', 'Grulla',\
          'Liver Chestnut', 'Other', 'Overo', 'Palomino', 'Perlino',\
          'Piebald', 'Pinto', 'Roan', 'Sabino', 'Sil', 'Sorrel', 'Tobiano',\
          'Tovero', 'White']

SEXES = ['Broodmare', 'Colt', 'Filly', 'Foal', 'Gelding', 'Mare', 'Ridgling',\
         'Stallion', 'Unborn Foal', 'Weanling', 'Yearling']


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
        self.df = self.clean_up(self.df)
        print 'data cleaned...'
        self.fit_most_common_values()
        self.fillna()
        print 'na filled...'
        self.engineer_features()
        return self.select_features()

    def transform(self, feature_dict):
        '''
        INPUT: dictionary
        OUTPUT: 2D numpy array

        Transforms input dataframe to meet the format required to serve as
        input data into a model.
        '''
        df = pd.Series(feature_dict).to_frame().transpose()
        df = self.clean_up(df, fit=False)
        cols = self.final_columns
        cols.remove(u'_id')
        return df[cols].values


    def clean_prices(self, series):
        '''
        INPUT: pandas series
        OUTPUT: 1D numpy array

        Cleans target variable "Price" independent of other features.
        '''
        series = series.apply(self.clean_price)
        return series.values

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


    def clean_up(self, df, fit=True):
        '''
        INPUT: dataframe, boolean
        OUTPUT: dataframe

        Cleans data into consistent format and datatypes.
        '''
        # Create Dummy Variables
        df['Skills / Disciplines'] = df['Skills / Disciplines'].fillna(u'-')
        df['Skills / Disciplines'] = df['Skills / Disciplines']\
                                     .apply(lambda y: [] if y == u'-'
                                            else y.split(', '))
        # skills = Counter([x for y in df['Skills / Disciplines'] for x in y])
        for skill in SKILLS:
            df['Skill_' + skill] = df['Skills / Disciplines']\
                                   .apply(lambda x: 1\
                                    if unicode(skill) in x else 0)
        df.drop('Skills / Disciplines', axis=1, inplace=True)
        for breed in BREEDS:
            df['Breed_' + breed] = df['Breed']\
                                   .apply(lambda x: 1\
                                          if Breeds_dict[x] == breed else 0)
        df.drop('Breed', axis=1, inplace=True)
        for color in COLORS:
            df['Color_' + color] = df['Color']\
                                   .apply(lambda x: 1\
                                          if Color_dict[x] == color else 0)
        df.drop('Color', axis=1, inplace=True)
        for sex in SEXES:
            df['Sex_' + sex] = df['Sex'].apply(lambda x: 1\
                                               if x == unicode(sex) else 0)
        df.drop('Sex', axis=1, inplace=True)
        # Replace missing values '-' by None
        df = df.apply(lambda x: x.apply(lambda y: None if y == u'-' else y))
        
        # Apply individual clean up functions to columns
        df['Height (hh)'] = df['Height (hh)'].apply(self.clean_height)
        df['Temperament'] = df['Temperament'].apply(lambda x: eval(x + '.')\
                                                    if isinstance(x, unicode)\
                                                     else None)
        df['Weight (lbs)'] = df['Weight (lbs)'].astype('float')\
                                               .apply(lambda x: None\
                                                      if x > 3000 else abs(x))
        if fit:
            df['Ad Created'] = df['Ad Created'].apply(self.clean_date)
            df['Foal Date'] = df['Foal Date'].apply(self.clean_date)
            df['Last Update'] = df['Last Update'].apply(self.clean_date)
        else:
            df['Age'] = df['Age'].apply(lambda x: float(x))    
        return df
    
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

        Determines and stores most common value for all columns.
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



