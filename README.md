# Smart Parking System Front-End UI

For our smart parking garage system, we used the NiceGUI library to build the frontend UI to run in a web browser. The UI interfaces with the RESTful API
backend to interact with system data through HTTP requests, as well as the pricing microservice.

# Table of Contents
1. [Features](#features)
2. [Installation & Running the application](#installation)
3. [Docker Deployment](#docker)

## Features <a name="features"></a>

- Browser based UI
- User account signup and login
- Garage overview and availability
- Real-time pricing estimates
- Reservation management


## Installation <a name="installation"></a>

### 1. Create a Python Virtual Environment

First, navigate to the `/Front-End` directory and create a virtual environment:

```sh
python -m venv .venv
```

### 2. Activate the Virtual Environment

Activate the virtual environment:

- On Windows:
    ```sh
    .\.venv\Scripts\activate
    ```
- On macOS and Linux:
    ```sh
    source .venv/bin/activate
    ```

### 3. Install Dependencies

Install the required dependencies using `pip`:

```sh
pip install -r requirements.txt
```

### 4. Run the Program

From the `/Front-End` directory run:

```sh
python app/main.py
```
- *Note*: This app is configured to run on port 80 to allow Azure to complete health checks and pass deployment. Should this cause issues for you,
change the port defined on line 28 of main.py to some alternative port.


## Docker Deployment <a name="docker"></a>

This app has been deployed to Azure as a Web App for containers. At the time of reading this, it will likely not be running since this is a school project and resources aren't free. I won't go very in detail on deploying to Azure, but I will give a very breif overview of the steps taken to deploy.
Obviously, you need docker installed on your system.

1. Create the dockerfile
2. Build the docker image (Do this in the same dir as your dockerfile)
    - `docker build -t <your_image_name>:<version>`
3. On Azure, create a Container Registry. Grab the login server hostname once this is deployed.
    - and also a new resource group
4. On your machine, login to the registry
    - `docker login something.azurecr.io`
    - Use admin credentials from the Access Keys page on Azure
5. Create an *Azure Ready* image of your most recent application image version
    - `docker tag <your_image_name>:<version> something.azurecr.io/<your_image_name>:latest`
    - For this project, I never change the :latest tag of the Azure image. This is so that every time I push a new version of the app, it automatically replaces the existing version (if you enabled continuous deployment)
6. Push to Azure
    - `docker push something.azurecr.io/<your_image_name>:latest`
7. Create a *Web App for Containers* resource on Azure using the image we just pushed. Google this for more info its pretty simple however.
    - deploy this and that's it.

#### Our web app deployment URL: [https://smartpark-ui-dkfqg0ghg9ezdge3.canadacentral-01.azurewebsites.net/](https://smartpark-ui-dkfqg0ghg9ezdge3.canadacentral-01.azurewebsites.net/)