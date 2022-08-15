Best Practices

Unit tests can be found in **tests** folder

Integration test can be found in **integration-test** folder

For linting and code formatting, the file **pyproject.toml** is used

Makefile is also present

For pre-commit hooks, **.pre-commit-config.yaml** is used

**NOTE** I have used SSH terminal for this section. I have provided the Pipfile if you are facing issues with the environment. You can create a virtual environment using Pipfile by running the command : pipenv install

More information on how to create a virtual environment using Pipfile can be found here : 
https://stackoverflow.com/questions/52171593/how-to-install-dependencies-from-a-copied-pipfile-inside-a-virtual-environment

**NOTE** : integration-test folder has **run.sh** file. You need to give permission before running it, or else you will get permission denied error.

You should be inside **code** directory. You can give permission to run.sh file by executing the following command in SSH terminal : 

**Command** : chmod +x integration-test/run.sh

**Steps to run unit tests, integration test, linting, code formatting** : 

1. Make sure you are inside code directory

2. Execute the following command : 

**Command** : make publish

This command will : 

* Run unit tests. There might be warnings related to sklearn version. You can ignore that. To configure Python Tests, please refer the video MLOps Zoomcamp 6.1 - Testing Python code with pytest, at time **6:09**
* Perform quality checks - linting and code formatting. It will reformat batch.py file by using "black"
* Build docker container and image
* Create a bucket in Localstack.
* Run integration test. Integration test will output the predicted wine quality and print the contents of bucket present in Localstack (input and output files)

Integration test uses Localstack to mimic S3 bucket. Instead of using actual S3 bucket to store and retrieve files, we are using Localstack. It works exactly like S3, but locally. 

**Steps to perform pre-commit hooks** :

1. Make sure you are inside **code** directory

2. Initialize empty Git repository by running the following command : 

**Command** : git init

3. Install pre-commit by running the following command : 

**Command** : pre-commit install

4. Check status of files by running the following command :

**Command** : git status

5. Add all the files by running the following command :

**Command** : git add .

**NOTE** : Please make sure "." is added at the end of above command

6. Commit the files by running the following command :

**Command** : git commit -m 'initial commit'

Here, either all tests will pass or some tests will fail. If you have already executed the command *make publish*, then all tests should pass. If not, then some tests will fail, but those files will be reformatted by pre-commit. Repeat Steps 4, 5, and 6 to add the files modified by pre-commit. 

Screenshots of logs of SSH terminal while executing the above commands have been saved to "results" folder for reference.