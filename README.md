# TODO-List

A simple TODO-List application developed using Python Flask. 

### Features
The application allows users to: 
- Sign in using Gmail, Facebook or Github login.
- Add a TODO item.
- Delete a TODO item.
- List all TODO items.
- Mark a TODO item as completed.

### Database
Data is stored in an SQLite database with the following design:
![Database design](/img/database_design.png)
- ``flask_dance_oauth``: a managed table that stores OAuth login info
- ``user``: stores user info
- ``task``: stores task info


## 1. Instruction for running the app

### 1.1 Running with Docker
1. Download the Docker image from Docker Hub
    ```Docker
    docker pull jiaju051631/todo-list:0.1
    ```
2. Download the ``docker-compose.yaml`` file from [GitHub](https://github.com/jiaju051631/todo-list)
3. Start the service with the Docker Compose file
    ```Docker
    docker-compose -f docker-compose.yaml up -d
    ```
4. Access the application at https://127.0.0.1:5000 on your host

### 1.2 Running with source repo
1. Download and install Python 3.8 or above from [here](https://www.python.org/downloads/)
2. Download the source code from GitHub
    ```Shell
    git clone https://github.com/jiaju051631/todo-list.git
    cd todo-list
    ```
3. Create a Python virtual environment and install all dependencies
    ```Shell
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
4. Run the Flask application, and the app will start to run at https://127.0.0.1:5000 on your host
    ```Python
    python app.py
    ```

## 2. Instruction for testing the app

The `pytest` library is used to perform the testing. Unit test scripts are saved in the `tests` directory. 

Each TODO list API is tested with valid and invalid access token. 

Test result:
![Test result](/img/test_result.png)

### 2.1 Testing with Docker
1. Start a container with the image 
    ```Docker
    docker run -d -p 5000:5000 --name "todo-list" jiaju051631/todo-list:0.1
    ```
2. Run the container in the interactive mode
    ```Docker
    docker exec -it todo-list /bin/sh
    ```
3. In the `/todo-list` directory, create a Python virtual environment. Activate it and install all dependencies
    ```Python
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
4. Execute the test cases using pytest
    ```Python
    pytest -v 
    ```

### 2.2 Testing with source repo
1. In the project folder, execute the test cases directly using pytest
    ```Python
    pytest -v 
    ```

## 3. Instruction for building the app

1. Create a Dockerfile with steps to build a Docker image from the application
2. Run the following command to build the image
    ```Docker
    docker build -t <image_name>:<tag> <path_to_Dockerfile>
    ```
    Example:
    ```Docker
    docker build -t todo-list:0.1 ./todo-list
    ```
2. Check the image built
    ```Docker
    docker image ls
    ```
    ![Docker image](/img/docker_image.png)

## 4. Interface documentation

### 4.1 User login
In the [index page](https://127.0.0.1:5000), three links are added for the user login feature. Each link will redirect the user to the login portal of the respective service provider
![User login](/img/user_login.png)

Upon successful login, the username will be displayed.
![User login success](/img/user_login_success.png)


### 4.2 TODO list item management 
There is no interface implemented for TODO list features. A registered user can send HTTP requests with an OAuth access token to interact with the server APIs.

The access token can be found in the ``flaks_dance_oauth`` table in the SQLite database. 
![OAuth access token](/img/access_token.png)

HTTP requests:
- Adding a TODO item
    ```Shell
    curl -X POST -H "Authorization: Bearer <access_token>" -k https://127.0.0.1:5000/task/add/<task%20name>
    ```
- Deleting a TODO item
    ```Shell
    curl -X DELETE -H "Authorization: Bearer <access_token>" -k https://127.0.0.1:5000/task/delete/<task_id>
    ```
- Listing TODO items
    ```Shell
    curl -X GET -H "Authorization: Bearer <access_token>" -k https://127.0.0.1:5000/task/list
    ```
- Marking a TODO item as complete
    ```Shell
    curl -X PUT -H "Authorization: Bearer <access_token>" -k https://127.0.0.1:5000/task/mark-complete/<task_id>
    ```