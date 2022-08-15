Experiment Tracking and Model Registry

This section aims to perform experiment tracking and register best models using MLflow. 

File Structure : 

1. preprocess.py -> This script loads the raw data from input folder, processes it and saves the pre-processed data in output folder.

2. train.py -> The script will load the pre-processed data from output folder, train the model on the training set and calculate the RMSE on the validation set. The script logs the parameters and artifacts in MLflow(locally) as well as logs the artifacts in S3 bucket(cloud).

3. hpo.py -> This script tries to reduce the validation error by tuning the hyperparameters of the random forest regressor using hyperopt. The script logs the parameters and artifacts in MLflow(locally) as well as logs the artifacts in S3 bucket(cloud).

4. register_model.py -> This script will promote the best model (with lowest test_rmse) to the model registry. It will check the results from the previous step and select the top 5 runs. After that, it will calculate the RMSE of those models on the test set and save the results to a new experiment called "red-wine-random-forest-best-models". The model with lowest test RMSE from the 5 runs is registered.

**Artifacts can be saved locally as well as on cloud (AWS). My script saves these artifacts in S3 bucket. It meets the requirement of developing project on Cloud (mentioned in README of course project of MLOps Zoomcamp Github Repo).**

The scripts use SQLite as backend and Cloud (AWS S3) for storing the artifacts.

Before running any commands, **please create a S3 bucket in your AWS account**. The scripts will log artifacts in your S3 bucket. It will also log in MLflow, locally
(http://127.0.0.1:5000)

For accessing AWS services using CLI, please configure your aws credentials. It can be done in SSH terminal/Anaconda Prompt by running the command : aws configure

It will ask you for your :

1. AWS Access Key ID
2. AWS Secret Access Key
3. Default region name
4. Default output format

Please enter the credentials above before running the scripts.

These credentials have profile name as "default". I recommend to use your default AWS profile for running the scripts so that you won't need to make any changes in the python scripts provided. However, if you wish to use any other AWS profile other than the "default" one, then please make changes in credentials and config files accordingly. These files are located at **~/.aws/credentials** for Linux and Mac and at **%USERPROFILE%\.aws\credentials** for Windows. More information on setting up profile can be found at : 
https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-profiles.html

If you use any other AWS profile other than "default", then you will have to make some changes in train.py, hpo.py and register_model.py. These changes are discussed later in this document.

**NOTE** : I have used Anaconda Prompt for this section instead of SSH terminal because I was having issues with sklearn version in SSH terminal. If you face any errors while running the script, please consider creating a new environment using the requirements.txt file.

**Steps to create anaconda environment** :

1. conda create -n test_env python=3.9

2. pip install -r requirements.txt

Before running the scripts, open 2 SSH terminal/Anaconda Prompt - Terminal 1 and Terminal 2.

**Steps to run the scripts** :

1. In terminal 1, start the MLflow server using the following command :

**Command** : mlflow server --backend-store-uri=sqlite:///mlflow.db --default-artifact-root=s3://{bucket-name}/

If your S3 bucket name is mlops-zoomcamp-project, the command should look like : 

mlflow server --backend-store-uri=sqlite:///mlflow.db --default-artifact-root=s3://mlops-zoomcamp-project/

**NOTE** : The server should keep running, and you should go to terminal 2 to execute the scripts.

2. Go to terminal 2, and execute the script preprocess.py. This script loads the raw data from input folder, preprocesses it and saves the pre-processed data in output folder. Run the script using the following command : 

**Command** : python preprocess.py

3. Make sure the server from step-1 is up and running. After the execution of step-2 is finished, execute the script train.py in terminal 2. The script will load the datasets produced by the previous step, train the model on the training set and calculates the RMSE on the validation set. The script logs the parameters and artifacts in MLflow(locally) as well as logs the artifacts in S3 bucket(cloud). Run the script using the following command : 

**Command** : python train.py

**NOTE** If you use other AWS profile other than "default", then please go to **line number 9** of train.py and change the os.environ["AWS_PROFILE"] variable to your profile name before executing the script. If the profile name is "user1", then line number 9 should look like : os.environ["AWS_PROFILE"] = "user1"

4. After the execution of step-3 is finished, execute the script hpo.py in terminal 2. This script tries to reduce the validation error by tuning the hyperparameters of the random forest regressor using hyperopt. The script logs the parameters and artifacts in MLflow(locally) as well as logs the artifacts in S3 bucket(cloud). Run the script using the following command :

**Command** : python hpo.py

**NOTE** If you use other AWS profile other than "default", then please go to **line number 12** of hpo.py and change the os.environ["AWS_PROFILE"] variable to your profile name before executing the script. If the profile name is "user1", then line number 12 should look like : os.environ["AWS_PROFILE"] = "user1"

5. After the execution of step-4 is finished, execute the script register_model.py in terminal 2. This script will promote the best model (with lowest test_rmse) to the model registry. It will check the results from the previous step and select the top 5 runs. After that, it will calculate the RMSE of those models on the test set and save the results to a new experiment called "red-wine-random-forest-best-models". 

For model registry, out of the 5 runs in "red-wine-random-forest-best-models" experiment, the run with lowest test_rmse is registered. You can view the registered model at **http://127.0.0.1:5000/#/models** 

The script logs the parameters and artifacts in MLflow(locally) as well as logs the artifacts in S3 bucket(cloud). Run the script using the following command :

**Command** : python register_model.py

**NOTE** If you use other AWS profile other than "default", then please go to **line number 13** of register_model.py and change the os.environ["AWS_PROFILE"] variable to your profile name before executing the script. If the profile name is "user1", then line number 13 should look like : os.environ["AWS_PROFILE"] = "user1"

Experiments and models(and artifacts) can be viewed locally at http://127.0.0.1:5000 Registered model can also be viewed at http://127.0.0.1:5000/#/models

To view the artifacts on cloud, please visit your AWS S3 bucket. Your bucket will have 3 folders named "1/", "2/", and "3/". These 3 folders will have artifacts of the models which were logged by running the 3 scripts train.py, hpo.py, and register_model.py respectively. Refresh the website if these folders are not visible in your S3 bucket.

Images of experiments and registered model from MLflow and S3 bucket which stores artifacts, are saved to "results" folder for reference.