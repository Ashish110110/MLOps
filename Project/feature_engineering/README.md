Feature Engineering

In this section, I have selected top 4 independent variables from the dataset which best predict the red wine quality using SelectKBest class of sklearn. "chi2" method is used as scoring function. 

I have used linear regression to predict red wine quality. I have saved the DictVectorizer and linear regression model as lin_reg.bin, which will be used as input model in other sections.

**Steps to run the script** :

1. Run all the cells of model.ipynb. It will generate lin_reg.bin file, which will be used in other sections.