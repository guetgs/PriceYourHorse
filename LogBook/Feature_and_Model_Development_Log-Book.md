# Feature and Model Development Log-Book
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
![Predicted vs Real Plot of Sample](figure_1_PvsY_sample.png)
#####All Data:
R^2: 0.952
OOB: 0.779
![Predicted vs Real Plot of all Data](figure_2_PvsY_all.png)

### Second Model
Remove Price Outliers (> 3*Std)
#####All Data:
R^2: 0.882
OOB: 0.288
![Predicted vs Real Plot of all Data without outliers](figure_3_PvsY_all_without_outlier.png)

### Tabular Feature Engineering
Breeds: Keep all except categories with single values.
![Boxplot prices vs. breeds](figure_6_boxplot_price_breed_zoomin.png)

Colors: Classify in Brindle, Grey, Piebald, Other
![Boxplot prices vs. colors](figure_8_boxplot_price_color_zoominmore.png)

Sexes: Classify into Broodmare, Unborn Foal, Ridgling, Adult, Colt/Filly, Foal/Yearling
![Boxplot prices vs. sexes](figure_9_boxplot_price_sex_zoominmore.png)

Temperament: Classify into Extreme vs Intermediate Temperament
![Boxplot prices vs. temperament](figure_9_boxplot_price_temperament_zoomin.png)

Weight: Discard Weight
![Boxplot prices vs. weight](figure_10_boxplot_price_weight_zoomin.png)



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
![Predicted vs Real Plot of all Data without outliers, first feature engineering step](figure_14_PvsV_allwo_outlier_engineeredtabularfeatures.png)
