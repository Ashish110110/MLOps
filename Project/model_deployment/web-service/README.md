# Model Deployment

This section aims to deploy model as web-service using Flask and Docker. The model deployment code is containerized.

**NOTE :** I have used SSH terminal for this section. I have provided the Pipfile if you are facing issues with the environment. You can create a virtual environment using Pipfile by running the command : pipenv install

More information on how to create a virtual environment using Pipfile can be found here : 
https://stackoverflow.com/questions/52171593/how-to-install-dependencies-from-a-copied-pipfile-inside-a-virtual-environment

## Steps to run the script in SSH terminal using Flask

1. Open two terminal windows, Terminal 1 and Terminal 2.

2. In terminal 1, to start the server, execute the following command :

   **Command :** python predict.py

**NOTE :** The server should keep running, and you should go to terminal 2 to execute the test script.

1. In terminal 2, execute the following command :

   **Command :** python test.py

This will send numerical features (total_sulfur_dioxide, free_sulfur_dioxide, alcohol, volatile_acidity) to the server, and server will send predicted wine quality based on the features. You can edit the numerical features in test.py, if you wish.

## Steps to run the script in terminal using Docker

1. Stop the web services running in terminal 1. For Windows, it can be stopped using CTRL + C

2. Here, we are using docker to run the model. The code is containerized. In terminal 1, execute the following commands :

   **Command-1 :** docker build -t red-wine-prediction:v1 .

This command will build a Docker image "red-wine-prediction" from the Dockerfile.

**NOTE :** Do not forget to include the "." at the end of Command-1

**Command-2 :** docker run -it --rm -p 9696:9696 red-wine-prediction:v1

This command will start the gunicorn server. 

**NOTE :** The services should keep running, and you should go to terminal 2 to execute the test script.

3. To get response from the server, execute the following command in terminal 2 : 

   **Command :** python test.py

This will send numerical features (total_sulfur_dioxide, free_sulfur_dioxide, alcohol, volatile_acidity) to the server, and server will send predicted wine quality based on the features. You can edit the numerical features in test.py, if you wish.

Screenshots of logs in SSH terminal are saved in "results" folder for reference.