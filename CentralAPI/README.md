# Smart Parking System Central REST API

For our smart parking garage system, we built the backend in the <a href="https://fastapi.tiangolo.com/">FastAPI</a> python library. This library has several built-in tools that make route and endpoint definition, data validation, and continuous development very easy. We connect to a MongoDB cluster for system data storage and retrival. The API publishes messages through a RabbitMQ server to the sensor nodes simulating the parking garage spaces. It also communicates with the pricing microservice to fetch reservation pricing at a given time.

# Table of Contents
1. [Features](#features)
2. [Installation & Running the application](#installation)
3. [Docker Deployment](#docker)
4. [Summary of Routes & Endpoints](#endpoints)

## Features <a name="features"></a>

- Automatic interactive API docs
- Authentication mechanisms built in (but not used for routes for simplicity of this project)
- Custom defined pydantic models for data validation


## Installation <a name="installation"></a>

- *Note*: This repository is configured to use environment variables to obscure the service host URLs. However, a .env file is provided. To use this application locally and connect to our other services, uncomment the first 2 lines of main.py. If you are running the entire system locally, then you will need to adjust these URLs to point to your local URLs.

### 1. Create a Python Virtual Environment

First, navigate to the `/Central-API` directory and create a virtual environment:

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

From the `/Central-API` directory run:

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

#### Our web app deployment URL: [https://central-api-gud7ethebpctcag5.canadacentral-01.azurewebsites.net/](https://central-api-gud7ethebpctcag5.canadacentral-01.azurewebsites.net/)


## Summary Of Routes and Endpoints <a name="endpoints"></a>

Provided the API is still up and running on Azure, you can view the API documentation <a href="https://central-api-gud7ethebpctcag5.canadacentral-01.azurewebsites.net/docs">here.</a>

- #### Auth:
    - POST /signup - Creates a user using UserCreate model, returns UserSignUp.
    - POST /login - Logs in a user, returns Token.

- #### Users:
    - GET /users - Gets all users with optional filters, returns ListResponse[User]
    - GET /users/{id} - Gets a user by ID, returns User
    - PUT /users/{id} - Updates current user using UserUpdate model, returns User
    - DELETE /users/{id} - Deletes a user. Does not return content, only a 204 status code.

- #### Spots:
    - GET /spots - Gets all spots, returns ListResponse[ParkingSpot]
        - allows filtering of the form {field}:{operator}:{value} where field is the ParkingSpot field to be filtered by, operator is a logical operator like eq, gt, lt, and value is the value of the expression
        - this filter is appended to the url as a filter parameter
        - Eg. filtering the records by only spots that have a vacant status: https://central-api-gud7ethebpctcag5.canadacentral-01.azurewebsites.net/spots?filter=status%3Aeq%3Avacant
    - GET /spots/{id} - Gets a spot by ID, returns ParkingSpot
    - POST /spots - Creates a spot using ParkingSpotBase model, returns ParkingSpot
    - PUT /spots/{id} - Updates a spot by ID using ParkingSpotUpdate model, returns ParkingSpot
    - DELETE /spots/{id} - Deletes a spot. Does not return content, only a 204 status code.

- #### Reservations:
    - GET /reservations - Gets all reservations, allows filtering, returns ListResponse[Reservation]
        - allows filtering of the form {field}:{operator}:{value} where field is the Reservation field to be filtered by, operator is a logical operator like eq, gt, lt, and value is the value of the expression
        - this filter is appended to the url as a filter parameter
        - Eg. filtering the records by only reservations that start after 2025-03-29T18:00:00: https://central-api-gud7ethebpctcag5.canadacentral-01.azurewebsites.net/reservations?filter=start_time%3Agt%3A2025-03-29T18%3A00%3A00
    - GET /reservations/{id} - Gets a reservation by ID, returns Reservation
    - POST /reservations - Creates a reservation using the ReservationCreate model, returns Reservation
    - DELETE /reservations/{id} - Deletes a reservation, returns nothing (204)