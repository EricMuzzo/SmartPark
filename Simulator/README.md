# Smart Parking System Simulator

For our smart parking garage system, we built a component that simulates several IoT sensors monitoring parking spaces. These simulators serve 2 main purposes:
- Randomly simulating drivers pulling into and out of parking spaces like a real garage
- Handling reservation notificates from the server to reserve a spot

This component recieves reservation notifications via a RabbitMQ channel, with each simulator process only consuming messages from the channel with the routing key matching their id.

# Table of Contents
1. [Installation & Running the application](#installation)
2. [Docker Deployment](#docker)


## Installation <a name="installation"></a>

### 1. Create a Python Virtual Environment

First, navigate to the `/Simulator` directory and create a virtual environment:

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

From the `/Simulator` directory run:

```sh
python simulator.py
```


## Docker Deployment <a name="docker"></a>

This app has been deployed to Azure as a container instance. At the time of reading this, it will likely not be running since this is a school project and resources aren't free. I won't go very in detail on deploying to Azure, but I will give a very breif overview of the steps taken to deploy.
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
7. Create a *Container Instance* resource on Azure using the image we just pushed. Google this for more info its pretty simple however.
    - deploy this and that's it.

#### Our container IP: 130.107.131.86