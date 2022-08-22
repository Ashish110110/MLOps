# MLOps Zoomcamp Project - Red Wine Quality Prediction

This is my project for MLOps Zoomcamp from DataTalks.Club

## Objective

Wine is differentiated according to its smell, flavor, and color. Judging the quality of wine manually is a tough task. Even the professional wine tasters don't have 100% accuracy. The Master Sommelier Diploma Exam is the world's most challenging wine tasting examination and only a few hundred people have passed it. So how do we decide that wine is good or bad? 

This project aims to solve the above problem. The aim of this project is to identify the features that best predict the quality of red wine and to produce insights into how each of these features affects the red wine quality in the model. Understanding how each feature will impact the red wine quality will help producers, distributors and companies in the red wine sector to better evaluate their production, distribution and pricing strategy.

I have used Red Wine Quality dataset. It can be found [here](https://www.kaggle.com/datasets/uciml/red-wine-quality-cortez-et-al-2009).

## Project Structure

The project is implemented on virtual machine Ubuntu 22.04 using AWS. The steps for each section for reproducbility are based on specific AWS configuration and may be different for different platforms (GCP, Azure). To reproduce the project without running into issues, I recommend to prepare the virtual environment as shown [here](https://www.youtube.com/watch?v=IXSiYkP23zo&list=PL3MmuxUbc_hIUISrluw_A7wDSmfOhErJK&index=4). Create EC2 instance as shown in the video. Using any different platform may cause bugs. 

I have made separate directory for each criteria mentioned in README of [MLOps Zoomcamp Course Project](https://github.com/DataTalksClub/mlops-zoomcamp/tree/main/07-project)

The directories are : 

1. feature_engineering   
2. experiment_tracking_and_model_registry
3. workflow_orchestration
4. model_deployment
5. model_monitoring
6. best_practices

Each directory has a README file in it which has the instructions on how to run the code. Also, each directory has Pipfile in it. So if you face any issues with virtual environment, you can use the Pipfile to create a new virtual environment.

More information on how to create a virtual environment using Pipfile can be found [here](https://stackoverflow.com/questions/52171593/how-to-install-dependencies-from-a-copied-pipfile-inside-a-virtual-environment)



## Tools and Technologies Used 

* Cloud : AWS
* Experiment Tracking and Model Registry : MLflow
* Workflow Orchestration : Prefect
* Containerization : Docker and Docker Compose
* Model Deployment : Deployment as web service using Flask, Docker, MLflow and AWS
* Model Monitoring : Evidently AI, Grafana and Prometheus
* Best Practices : Unit tests, Integration test, Linting, Code Formatting, Makefile and Pre-commit hooks


**NOTE :** For peer reviewing process, please download the repository as zip file instead of cloning it using Git bash. You will run into issues while reviewing best_practices section of the project if you clone the repository.
