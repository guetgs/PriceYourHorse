# PriceYourHorse: Timeline
### Due Monday, Nov 9
-  [x] Initialize Github repo
-  [x] Update data collection
-  [x] Implement feature extraction module
-  [x] Run feature extraction into new mongodb table
-  [x] Implement preprocessor class (basic version)
	- [x] Implement data cleanup method
	- [x] Implement feature engineering method
	- [x] Implement filling missing values method
	- [x] Implement feature selection method
	- [x] Outline tranform only method to be used to prepare user input data

### Due Tuesday, Nov 10
- [x] Implement model class (basic version)
	- [x] Implement fit-transform method
	- [x] Implement predict method
	- [x] Implement score method
	- [x] Implement crossvalidation method

### Due Wednesday, Nov 11
- [x] Implement web application (basic version)
	- [x] Select bootstrap template
	- [x] Implement skeleton for all views
	- [x] Implement user input form view
	- [x] Implement prediction view

### Due Thursday, Nov 12
- [x] Implement preprocessor transform method to process user input data
- [x] Update preprocessor class to process text descriptions
	- [x] Update cleanup method
	- [x] Implement text vectorizer method
	- [x] Update feature selection method
	
### Due Friday, Nov 13
- [x] Update web application
	- [x] Implement description page
	- [x] Implement author information page
- [x] Update preprocessor
	- [x] Update feature selection using Random Forest Feature Importance

### Due Monday, Nov 16
- [x] Save trained vectorizer external of preprocessor to enable storage
	- [x] Implement Processor
	- [x] Implement Vectorizer
	- [x] Perform preprocessing outside of Processor class, to similarize entries from training set and from web application
- [x] Implement missing value predictor class
	- [x] Implement horse to horse similarity score method
	- [x] Implement k-means to identify centroids of similar horses
	- [x] Implement missing value prediction method
- [ ] Run K-means on whole dataset

### Due Tuesday, Nov 17
- [x] Update vocabulary
	- [x] Perform feature selection of text features
- [x] Implement predicted price range

### Due Wednesdy, Nov 18
- [x] Optimize model choice and parameter choice based on crossvalidation
- [x] Optimize feature selection for choosen model

### Due Thursday, Nov 19
- [x] Adjust user entry form of web application to the final feature selection
- [x] Update Readme of Github repo
- [x] Polish look of web application
- [x] Polish all functions and github repo


### Due Friday, Nov 20
- [x] Polish LogBook
- [x] Implement 3min power point presentation of the project


### Due Saturday, Nov 21
- [x] Update the details page of the web-application
- [x] Final polish on web application and powerpoint presentation