# Model Deployment

This section aims to deploy the model to AWS S3 bucket(Cloud).

**NOTE :** I have used SSH terminal for this section. I have provided the Pipfile if you are facing issues with the environment. You can create a virtual environment using Pipfile by running the command : pipenv install

More information on how to create a virtual environment using Pipfile can be found [here](https://stackoverflow.com/questions/52171593/how-to-install-dependencies-from-a-copied-pipfile-inside-a-virtual-environment)

Before running any commands, **please create a S3 bucket in your AWS account**. The scripts will deploy the model in this bucket.

For accessing AWS services using CLI, please configure your aws credentials. It can be done in SSH terminal/Anaconda Prompt by running the command : aws configure

It will ask you for your :

1. AWS Access Key ID
2. AWS Secret Access Key
3. Default region name
4. Default output format

Please enter the credentials above before running the scripts.

## Steps to execute the script

1. Open 3 terminal windows. Terminal 1, Terminal 2, and Terminal 3. In all the terminals, activate virtual environment which has the libraries mentioned in Pipfile. You should be inside web-service-mlflow directory in all the 3 terminals.

2. In Terminal 1, type the following command :

   **Command :** mlflow server --backend-store-uri=sqlite:///mlflow.db --default-artifact-root=s3://{bucket-name}/

Replace {bucket-name} with the name of bucket you created in your AWS account in step 1. 

For example, if you create a bucket "mlops-zoomcamp-project", the command should look like : 

mlflow server --backend-store-uri=sqlite:///mlflow.db --default-artifact-root=s3://mlops-zoomcamp-project/

**NOTE :** The server in terminal 1 should keep running, and you should go to terminal 2 to execute other scripts.

3. After executing the command in step 2, run all the cells in **random-forest-mlflow.ipynb**. It will train and log model in MLflow and the S3 bucket you created earlier.

4. In this step, you need to export the RUN_ID of the model which was logged to your S3 bucket. Go to your AWS account and open S3 (buckets).

RUN_ID can be found at : Amazon S3 > Buckets > {bucket-which-you-created-earlier} > 1/ > {RUN_ID}

For example, if bucket name is "mlops-zoomcamp-project", RUN_ID can be found at : Amazon S3 > Buckets > mlops-zoomcamp-project > 1/ > {RUN_ID}.

5. Open Terminal 2, and export the RUN_ID you got from step 4. If RUN_ID is 123456, then it can be exported via the following command : 

   **Command :** export RUN_ID="123456"

6. Before running predict.py, you need to enter the name of your bucket which you created earlier. **Go to line number 9 of predict.py**, and enter the name of your S3 bucket. 

For example, if you create a bucket "mlops-zoomcamp-project", then line number 9 should look like :

logged_model = f's3://mlops-zoomcamp-project/1/{RUN_ID}/artifacts/model'

7. Now in Terminal 2, after exporting the RUN_ID and entering bucket name in predict.py, execute the following command : 

   **Command :** python predict.py

This command will start the server, which waits for incoming data.

**NOTE :** The server in terminal 2 should keep running, and you should go to terminal 3 to execute other scripts.

8. Open Terminal 3, and execute the following command : 

   **Command :** python test.py

This command will send numerical features (total_sulfur_dioxide, free_sulfur_dioxide, alcohol, volatile_acidity) to the server, and print the model version which has been trained and logged in MLflow and your S3 bucket. It will also print the predicted wine quality based on the features we have sent. You can edit the numerical features in test.py, if you wish.

You can view the logged model in MLflow (http://127.0.0.1:5000) as well as in the S3 bucket you created earlier.

Screenshots of MLflow, S3 bucket and logs of SSH terminal are saved in "results" folder for reference.
