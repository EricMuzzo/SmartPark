# Smart Parking System Pricing Microservice

For our smart parking garage system, we separated the pricing calculator into a separate microservice. This final saved pricing in a reservation can only be fetched **BY** the API **FROM** the pricing microservice, preventing an injection from the client. This application was built using the <a href="https://fastapi.tiangolo.com/">FastAPI</a> python library. Upon receiving a timestamped request for pricing, the service returns a calculated rate per minute based on the garage's current demand.


# Table of Contents
1. [Installation & Running the application](#installation)
2. [Docker Deployment](#docker)
3. [Summary of Routes & Endpoints](#endpoints)


## Installation <a name="installation"></a>

- *Note*: This repository is configured to use environment variables to obscure the service host URLs. However, a .env file is provided. To use this application locally and connect to our other services, uncomment the first 2 lines of main.py. If you are running the entire system locally, then you will need to adjust these URLs to point to your local URLs.

### 1. Create a Python Virtual Environment

First, navigate to the `/Pricing Service` directory and create a virtual environment:

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

From the `/Pricing Service` directory run:

```sh
fastapi dev app/main.py     #development mode
```

```sh
fastapi run app/main.py     #deployment mode
```


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

#### Our web app deployment URL: [https://smart-park-pricing-service-a8gwb6awatbehkh8.canadacentral-01.azurewebsites.net/](https://smart-park-pricing-service-a8gwb6awatbehkh8.canadacentral-01.azurewebsites.net/)


## Summary Of Routes and Endpoints <a name="endpoints"></a>

Provided the API is still up and running on Azure, you can view the API documentation <a href="https://smart-park-pricing-service-a8gwb6awatbehkh8.canadacentral-01.azurewebsites.net/docs">here.</a>

- #### Default:
    - POST /calculate-rate - Returns the pricing rate per minute.