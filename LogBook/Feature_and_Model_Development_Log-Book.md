# Feature and Model Development Log-Book
## Feature optimization
### First Model
#####Features:
- Skills / Disciplines Dummy Variables
- Height (hh) as float (outlier removed, inches converted to hh
- Temperament as float
- Weigth (lbs) as float (outlier removed)
- Age as float (derived from Foal Date)
- Breed as Dummy Variables (no selection)
- Color as Dummy Variables (no selection)
- Sex as Dummy Variables (no selection)
- Pedigree is Dummy Variable

#####Model:
Sklearn's RandomForestRegressor

Parameters:

- n_estimators: 100
- max_features: auto
- oob_score: True

#####Sample Data:
R^2: 0.406
OOB: -0.255
![Predicted vs Real Plot of Sample](figures/figure_1_PvsY_sample.png)
#####All Data:
R^2: 0.952
OOB: 0.779
![Predicted vs Real Plot of all Data](figures/figure_2_PvsY_all.png)

### Second Model
Remove Price Outliers (> 3*Std)
#####All Data:
R^2: 0.882
OOB: 0.288
![Predicted vs Real Plot of all Data without outliers](figures/figure_3_PvsY_all_without_outlier.png)

### Tabular Feature Engineering
Breeds: Keep all except categories with single values.
![Boxplot prices vs. breeds](figures/figure_6_boxplot_price_breed_zoomin.png)

Colors: Classify in Brindle, Grey, Piebald, Other
![Boxplot prices vs. colors](figures/figure_8_boxplot_price_color_zoominmore.png)

Sexes: Classify into Broodmare, Unborn Foal, Ridgling, Adult, Colt/Filly, Foal/Yearling
![Boxplot prices vs. sexes](figures/figure_9_boxplot_price_sex_zoominmore.png)

Temperament: Classify into Extreme vs Intermediate Temperament
![Boxplot prices vs. temperament](figure_9_boxplot_price_temperament_zoomin.png)

Weight: Discard Weight
![Boxplot prices vs. weight](figures/figure_10_boxplot_price_weight_zoomin.png)



### Third Model
#####Features:
- Skills / Disciplines Dummy Variables (limited Skill set)
- Height (hh) as float (outlier removed, inches converted to hh)
- Temperament as dummy (extreme vs intermediate values)
- Age as float (derived from Foal Date)
- Breed as Dummy Variables (remove selected breeds)
- Color as Dummy Variables (reduced variable space)
- Sex as Dummy Variables (reduced variable space)
- Pedigree is Dummy Variable

#####Model:
Sklearn's RandomForestRegressor

Parameters:
- n_estimators: 100
- max_features: auto
- oob_score: True

#####All Data (prices < 60000):
R^2: 0.887
OOB: 0.332
![Predicted vs Real Plot of all Data without outliers, first feature engineering step](figures/figure_14_PvsV_allwo_outlier_engineeredtabularfeatures.png)

### Fourth Model
#####Features:
- Skills / Disciplines merged with Descriptions, term-frequency matrix (strip_accents='unicode', stop_words='english', ngram_range=(1,2), min_df=100, use_idf=False)
- Height (hh) as float (outlier removed, inches converted to hh)
- Temperament as dummy (extreme vs intermediate values)
- Age as float (derived from Foal Date)
- Breed as Dummy Variables (remove selected breeds)
- Color as Dummy Variables (reduced variable space)
- Sex as Dummy Variables (reduced variable space)
- Pedigree is Dummy Variable

#####Model:
Sklearn's RandomForestRegressor

Parameters:
- n_estimators: 100
- max_features: auto
- oob_score: True

#####All Data (prices < 60000):
R^2: 0.918
OOB: 0.413
![Predicted vs Real Plot of all Data without outliers, term-frequency matrix for descriptions](figures/figure_15_PvsY_withdescription.png)

### Model 4a
Use inverse document frequency
#####Features:
- Skills / Disciplines merged with Descriptions, term-frequency matrix (strip_accents='unicode', stop_words='english', ngram_range=(1,2), min_df=100, use_idf=True)
- Height (hh) as float (outlier removed, inches converted to hh)
- Temperament as dummy (extreme vs intermediate values)
- Age as float (derived from Foal Date)
- Breed as Dummy Variables (remove selected breeds)
- Color as Dummy Variables (reduced variable space)
- Sex as Dummy Variables (reduced variable space)
- Pedigree is Dummy Variable

#####Model:
Sklearn's RandomForestRegressor

Parameters:
- n_estimators: 100
- max_features: auto
- oob_score: True

#####All Data (prices < 60000):
R^2: 0.920
OOB: 0.422
![Predicted vs Real Plot of all Data without outliers, tf-idf matrix for descriptions](figures/figure_18_PvsY_with_tf_idf_description.png)

### Model 4b
Model 4a using own tokenizer (nltk word_tokenizer, WordNetLemmatizer)


#####All Data (prices < 60000):
R^2: 0.916
OOB: 0.400
![Predicted vs Real Plot of all Data without outliers, tf-idf matrix for lemmatized descriptions](figures/figure_19_PvsY_lemmatized.png)

### Fifth Model
#####Features:
- Skills / Disciplines merged with Descriptions, term-frequency matrix (strip_accents='unicode', stop_words='english', ngram_range=(1,2), min_df=100, use_idf=False), topic extraction using NMF (12 topics), topic as single numeric column
- Height (hh) as float (outlier removed, inches converted to hh)
- Temperament as dummy (extreme vs intermediate values)
- Age as float (derived from Foal Date)
- Breed as Dummy Variables (remove selected breeds)
- Color as Dummy Variables (reduced variable space)
- Sex as Dummy Variables (reduced variable space)
- Pedigree is Dummy Variable

#####Model:
Sklearn's RandomForestRegressor

Parameters:
- n_estimators: 100
- max_features: auto
- oob_score: True

#####Trained only on data with price (prices < 60000):
R^2: 0.705
OOB: 0.224
![Predicted vs Real Plot of all priced Data without outliers, topic column](figures/figure_16_PvsY_topics_from_description.png)

### Sixth Model
#####Features:
- Skills / Disciplines merged with Descriptions, term-frequency matrix (strip_accents='unicode', stop_words='english', ngram_range=(1,2), min_df=100, use_idf=False), topic extraction using NMF (12 topics), topic dummy variables
- Height (hh) as float (outlier removed, inches converted to hh)
- Temperament as dummy (extreme vs intermediate values)
- Age as float (derived from Foal Date)
- Breed as Dummy Variables (remove selected breeds)
- Color as Dummy Variables (reduced variable space)
- Sex as Dummy Variables (reduced variable space)
- Pedigree is Dummy Variable

#####Model:
Sklearn's RandomForestRegressor

Parameters:
- n_estimators: 100
- max_features: auto
- oob_score: True

#####Trained only on data with price (prices < 60000):
R^2: 0.706
OOB: 0.230
![Predicted vs Real Plot of all priced Data without outliers, topic dummies](figures/figure_17_PvsY_topics_as_dummies.png)

### Seventh Model
#####Features:
- Skills / Disciplines merged with Descriptions, term-frequency matrix 
- TFidfVectorizer: strip_accents='unicode',\
                          stop_words='english',\
                          ngram_range=(1, 1),\
                          min_df=100,\
                          tokenizer=self.tokenizer,\
                          vocabulary=Vocab,\
                          use_idf=True

- Height (hh) as float (outlier removed, inches converted to hh)
- Temperament as dummy (extreme vs intermediate values)
- Age as float (derived from Foal Date)
- Breed as Dummy Variables (remove selected breeds)
- Color as Dummy Variables (reduced variable space)
- Sex as Dummy Variables (reduced variable space)
- Pedigree is Dummy Variable

#####Model:
Sklearn's RandomForestRegressor

Parameters:
- n_estimators: 100
- max_features: auto
- oob_score: True

#####Trained only on data with price (prices < 60000):
R^2: 0.917
OOB: 0.398
![Predicted vs Real Plot all priced Data without outliers, vocab](figures/figure_20_PvsY_lemmatized_vocab_only.png)


## Change in code: separate processor/vectorizer
###Run I:
#####Data:
Only horses with price
#####Features:
- Skills / Disciplines merged with Descriptions, term-frequency matrix, use vocab
- TFidfVectorizer: strip_accents='unicode',\
                          stop_words='english',\
                          ngram_range=(1, 1),\
                          min_df=100,\
                          tokenizer=tokenizer,\
                          vocabulary=Vocab,\
                          use_idf=True
- tokenizer: WordNetLemmatizer()
- Height (hh) as float (outlier removed, inches converted to hh)
- Temperament as float
- Age as float (derived from Foal Date)
- Breed as Dummy Variables (according to dict)
- Color as Dummy Variables (reduced variable space)
- Sex as Dummy Variables (reduced variable space)
- Pedigree is Dummy Variable
- Fillna method: mode for categorical, mean for numeric
- PRICE_RANGE = [0, 60000]

#####Model:
Sklearn's RandomForestRegressor

Parameters:
- n_estimators: 100
- max_features: auto
- oob_score: True

#####Trained only on data with price (prices < 60000):
R^2: 0.915
OOB: 0.393
![Predicted vs Real Plot separate vectorizer](figures/figure_21_PvsY_separate_preprocessing_vectorizing.png)

###Run II:
same as bevore, but
PRICE_RANGE = [150, 60000]
R^2: 0.918
OOB: 0.400
![Predicted vs Real Plot separate vectorizer](figures/figure_21_PvsY_more_than_150_separate_preprocessing_vectorizing.png)

###Run III:
same as bevore, but

MODEL_PARAMS = {'n_estimators': 100,
                'max_features': 'sqrt',
                'oob_score': True,
                'n_jobs': -1}

R^2: 0.921
OOB: 0.417
![Predicted vs Real Plot separate vectorizer](figures/figure_22_PvsY_more_than_150_separate_preprocessing_vectorizing_sqrt_max_features.png)

## Model optimization
### Current Random Forest Predictor against Default Models
Use 5-fold cross-validation
Default parameters for all models
Predictor Parameter: MODEL_PARAMS = {'n_estimators': 100,
                'max_features': 'sqrt',
                'oob_score': True,
                'n_jobs': -1}

![Model Comparison](figures/Model_Comp_1.png)

### Explore parameter space of other models
MODEL_PARAMS = {'n_estimators': 100,
                'max_features': 'sqrt',
                'oob_score': True,
                'n_jobs': -1}

RF_PARAMS = {'n_estimators': 100,
             'max_features': 5,
             'oob_score': True,
             'n_jobs': -1}

GB_PARAMS = {'loss': 'lad',
             'learning_rate': 0.1,
             'n_estimators': 100,
             'max_depth': 3,
             'max_features': 'sqrt',
             'alpha': 0.9}

SVR_PARAMS = {'kernel': 'rbf',
              'C': 0.1,
              'epsilon': 0.1}

![Model Comparison](figures/Model_Comp_2.png)

MODEL_PARAMS = {'n_estimators': 100,
                'max_features': 'sqrt',
                'oob_score': True,
                'n_jobs': -1}

RF_PARAMS = {'n_estimators': 100,
             'max_features': 20,
             'oob_score': True,
             'n_jobs': -1}

GB_PARAMS = {'loss': 'huber',
             'learning_rate': 0.1,
             'n_estimators': 100,
             'max_depth': 3,
             'max_features': 'sqrt',
             'alpha': 0.9}

SVR_PARAMS = {'kernel': 'rbf',
              'C': 0.5,
              'epsilon': 0.2}

![Model Comparison](figures/Model_Comp_3.png)

MODEL_PARAMS = {'n_estimators': 100,
                'max_features': 'sqrt',
                'oob_score': True,
                'n_jobs': -1}

RF_PARAMS = {'n_estimators': 200,
             'max_features': 20,
             'oob_score': True,
             'n_jobs': -1}

GB_PARAMS = {'loss': 'huber',
             'learning_rate': 0.05,
             'n_estimators': 200,
             'max_depth': 3,
             'max_features': 'sqrt',
             'alpha': 0.9}

SVR_PARAMS = {'kernel': 'poly',
              'C': 0.5,
              'epsilon': 0.2}

![Model Comparison](figures/Model_Comp_4.png)

MODEL_PARAMS = {'n_estimators': 100,
                'max_features': 'sqrt',
                'oob_score': True,
                'n_jobs': -1}

RF_PARAMS = {'n_estimators': 200,
             'max_features': 20,
             'oob_score': True,
             'n_jobs': -1}

GB_PARAMS = {'loss': 'ls',
             'learning_rate': 0.05,
             'n_estimators': 200,
             'max_depth': 3,
             'max_features': 'sqrt',
             'alpha': 0.9}

SVR_PARAMS = {'kernel': 'poly',
              'C': 0.5,
              'epsilon': 0.2}

![Model Comparison](figures/Model_Comp_5.png)

MODEL_PARAMS = {'n_estimators': 400,
                'max_features': 'sqrt',
                'oob_score': True,
                'n_jobs': -1}

RF_PARAMS = {'n_estimators': 200,
             'max_features': 20,
             'oob_score': True,
             'n_jobs': -1}

GB_PARAMS = {'loss': 'ls',
             'learning_rate': 0.05,
             'n_estimators': 200,
             'max_depth': 3,
             'max_features': 'sqrt',
             'alpha': 0.9}

SVR_PARAMS = {'kernel': 'poly',
              'C': 0.5,
              'epsilon': 0.2}
![Model Comparison](figures/Model_Comp_8_more_estimators.png)


### Use maximum of KDE as predicted value in Predictor
    def predict(self, X):
        preds = self.predictions(X)
        p = []
        for row in preds.T:
            fig = plt.figure()
            graph = sns.kdeplot(row.ravel(), shade=True, color='g', alpha=1)
            x,y = graph.get_lines()[0].get_data()
            ind = np.argmax(y)
            price = np.round(x[ind], decimals=-1)
            p.append(price)
            plt.close(fig)
            graph = None
        return np.array(p)
![Model Comparison](figures/Model_Comp_6_alternative_predict_function.png)

### Use median predicted value in Predictor
    def predict(self, X):
        preds = self.predictions(X)
        return np.median(preds, axis=0)
![Model Comparison](Model_Comp_7_median_prediction.png)


