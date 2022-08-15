# Workflow Orchestration

This section aims to fully deploy the workflow using Prefect. It also saves all the data to S3 bucket (cloud). 

I have demonstrated following services of Prefect in this section : 

1. Deployments
2. Storage (uploads data files to remote storage, S3)
3. Blocks
4. Work Queues and Agents

### Prefect Storage Concept

Storage lets us configure how flow code for deployments is persisted and retrieved by Prefect agents. Anytime we build a deployment, a storage block is used to upload the entire directory containing our workflow code (along with supporting files) to its configured location. This helps ensure portability of our relative imports, configuration files, and more.

If no storage is explicitly configured, Prefect will use LocalFileSystem storage by default. However, due to the inherit lack of portability (as per Prefect docs), I have used remote storage S3.

**Prefect Blocks Concept**

Blocks are a primitive within Prefect that enable the storage of configuration and provide an interface for interacting with external systems. Blocks are useful for configuration that needs to be shared across flow runs and between flows.



Before running any commands, **please create a S3 bucket in your AWS account**. The script will save data files to this S3 bucket.

For accessing AWS services using CLI, please configure your aws credentials. It can be done in SSH terminal/Anaconda Prompt by running the command : aws configure

It will ask you for your :

1. AWS Access Key ID
2. AWS Secret Access Key
3. Default region name
4. Default output format

Please enter the credentials above before running the scripts.

**NOTE** I have used SSH terminal for this section. I have provided the Pipfile if you are facing issues with the environment. You can create a virtual environment using Pipfile by running the command : pipenv install

More information on how to create a virtual environment using Pipfile can be found here : 
https://stackoverflow.com/questions/52171593/how-to-install-dependencies-from-a-copied-pipfile-inside-a-virtual-environment

**IMPORTANT-NOTE** I have used **Prefect 2.0.1** while working on this project. Please make sure the Prefect version in your virtual environment is **2.0.1**. Also, before installing Prefect 2.0.1, **delete the ".prefect" folder** from your SSH. It can be found at **"/home/ububtu/.prefect"**

Install Prefect 2.0.1 only after deleting the ".prefect" folder.


**Before executing the script, please make the following changes in orchestration.py** : 

1. In line number 74, please enter bucket name of the bucket you created earlier, and remove {}. 

For example, if you create a bucket with name mlops-zoomcamp-project, the bucket path will look like : bucket_path="mlops-zoomcamp-project/prefect-orion".

2. In line number 74, please enter the **AWS_ACCESS_KEY_ID** AND **AWS_SECRET_ACCESS_KEY** of your AWS account, so that the script can save the data files to your S3 bucket. Remove the {} from both, AWS_ACCESS_KEY_ID AND AWS_SECRET_ACCESS_KEY. 

For example if AWS_ACCESS_KEY_ID is abc and AWS_SECRET_ACCESS_KEY is xyz, the variables will look like : AWS_ACCESS_KEY_ID="abc" and AWS_SECRET_ACCESS_KEY="xyz".

### Steps to run the script in SSH terminal

Open 3 SSH terminal windows, Terminal 1, Terminal 2, Terminal 3. You should be inside workflow_orchestration directory in all the 3 terminals.

1. In Terminal 1, execute the following command : 

**Command** : prefect orion start

This will start Prefect. Let the service be running in this terminal. Go to Terminal 2, to execute other commands.

2. In Terminal 2, run the following command : 

**Command** : prefect config set PREFECT_API_URL=http://127.0.0.1:4200/api

3. In Terminal 2, run the following command : 

**Command** : 
prefect deployment build ./orchestration.py:main --name "mlops-prefect-aws-deployment" --storage-block s3/mlops-project-block -t mlops-project-orchestration

This command will :

* Generate the main-manifest.json and main-deployment.yaml files for the deployment based on my flow code and options.
* Create a block "mlops-project-block". This block stores data as files in S3 bucket. You can see the files in your S3 bucket(the bucket which you created earlier).    Refresh the website if the files aren't visible. 
* Uploads the flow files to the configured storage location. In my case, it will upload to S3 bucket.

4. In Terminal 2, run the following command :

**Command** : prefect deployment apply main-deployment.yaml

This command will create the deployment on the API with tag "mlops-project-orchestration" (from step 3)

5. In Terminal 2, run the following command :

**Command** : prefect deployment ls

Once the deployment has been created, you'll see it in the Prefect UI (**http://127.0.0.1:4200**) and can inspect it using in the CLI by running the above command.

6. In Terminal 2, run the following command : 

**Command** : prefect agent start -t mlops-project-orchestration

The above command creates a work queue and starts an agent and looks for work from queue.

7. Keep the service running in Terminal 2. Go to Terminal 3 and execute the following command : 

**Command** : prefect deployment run main/mlops-prefect-aws-deployment

**NOTE** : At the time of working on this section of the project, the documentation of Prefect 2.0.1 stated that Schedules will be added later and hence, the work queue might be empty, i.e., without any upcoming runs. Prefect is off beta now, and in stable version of Prefect (version 2.0.1 and above), they have removed the DeploymentSpec function, which we used in Prefect beta(as shown in videos). DeploymentSpec function was present in beta versions of Prefect(2.0b). It allowed us to mention a schedule for agents (Interval, Cron schedule) in our code itself. Now, if we want to schedule deployments, we have to either do it through UI or make some changes in the main-deployment.yaml file. 

If you wish to see scheduled deployments, either through UI or by making changes in the main-deployment.yaml file, then please visit this link :
https://orion-docs.prefect.io/concepts/schedules/

Flows, deployments, blocks and work queues can be viewed at : http://127.0.0.1:4200

Screenshots of flows, deployment, work queues, block, storage and S3 bucket are stored in "results" folder for reference.
