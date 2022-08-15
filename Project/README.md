**Dataset** : Red Wine Quality

**Link** : https://archive.ics.uci.edu/ml/datasets/wine+quality

**Problem Statement** :

Wine is differentiated according to its smell, flavor, and color. Judging the quality of wine manually is a tough task. Even the professional wine tasters don't have 100% accuracy. The Master Sommelier Diploma Exam is the world's most challenging wine tasting examination and only a few hundred people have passed it. So how do we decide that wine is good or bad? 

This project aims to solve the above problem. The aim of this project is to identify the features that best predict the quality of red wine and to produce insights into how each of these features affects the red wine quality in the model. Understanding how each feature will impact the red wine quality will help producers, distributors and companies in the red wine sector to better evaluate their production, distribution and pricing strategy.

**About the Dataset** :

The dataset contains a total of 12 variables, which were recorded for 1,599 observations.

The input variables (based on physicochemical tests) : 

1 - fixed acidity

2 - volatile acidity

3 - citric acid

4 - residual sugar

5 - chlorides

6 - free sulfur dioxide

7 - total sulfur dioxide

8 - density

9 - pH

10 - sulphates

11 - alcohol

The output variable (based on sensory data) :

12 - quality (score between 0 and 10)


**Project Structure** :

I have made separate directory for each criteria mentioned in README of MLOps Zoomcamp Course Project (https://github.com/DataTalksClub/mlops-zoomcamp/tree/main/07-project)

The directories are : 

1. feature_engineering   
2. experiment_tracking_and_model_registry
3. workflow_orchestration
4. model_deployment
5. model_monitoring
6. best_practices

Each directory has a README file in it which has the instructions on how to run the code. Also, each directory has Pipfile in it. So if you face any issues with virtual environment, you can use the Pipfile to create a new virtual environment.

More information on how to create a virtual environment using Pipfile can be found here : 
https://stackoverflow.com/questions/52171593/how-to-install-dependencies-from-a-copied-pipfile-inside-a-virtual-environment

