# Smart Parking System - COE892 Distributed Cloud Computing Final Project 2025

# Table of Contents
1. [About](#about)
2. [Overview](#overview)
3. [System Design & Architecture](#design)
    - [Central API](#api)
    - [Database](#db)
    - [IoT Sensor Simulator](#iot)
    - [RabbitMQ Message Broker](#rabbit)
    - [Pricing Microservice](#pricing)
    - [Frontend Web UI](#ui)
4. [Installation & Deployment](#deployment)
5. [Authors](#authors)



## About <a name="about"></a>

This project was built for the purposes of our final project assignment for COE892 - Distributed Cloud Computing at Toronto Metropolitan University. The objective of this project was to apply the distributed systems and cloud computing principles learned in the coourse to a real-life application.



## Overview <a name="overview"></a>

Our group selected a **Smart Parking System** as our project application. The aim of this application is to simulate a cloud-based parking garage system featuring IoT sensors that monitor parking space in real-time. Our pricing model is dynamically calculated in real-time based on the demand of the garage. Users of the system can interact with our UI to find parking and reserve spaces.



## System Design & Architecture <a name="design"></a>

The **Smart Parking System** is designed as a distributed cloud-based platform with 6 main components. To deploy our application to the cloud, Microsoft Azure was used to host our dockerized applications. Each application component has its own README describing its functionality, but a brief overview is given here.

- ### Central REST API Server <a name="api"></a>
    Built in Python using the FastAPI library, this component facilitates communication between all other components. It provides RESTful HTTP access to system resources and operations. The API is separated into 3 main routes; **Users, Spots,** and **Reservations**. It also has authentication functionality built in, but we decided not to protect routes with it for demo purposes.

    The source code and documentation can be found in the <a href="https://github.com/EricMuzzo/COE892Project-SmartPark-CentralAPI">Central API Repository</a>

    **Deployment URL:** [https://central-api-gud7ethebpctcag5.canadacentral-01.azurewebsites.net/](https://central-api-gud7ethebpctcag5.canadacentral-01.azurewebsites.net/)

    **API Interactive Docs**: [https://central-api-gud7ethebpctcag5.canadacentral-01.azurewebsites.net/docs](https://central-api-gud7ethebpctcag5.canadacentral-01.azurewebsites.net/docs)


- ### MongoDB Database <a name="db"></a>
    A Mongo cluster holds our system information in a NoSQL database featuring 3 collections:
    - **Users**: user record
    - **Spots**: single parking spot record
    - **Reservations**: reservation record


- ### IoT Sensor Simulator <a name="iot"></a>
    Built in python, this component is responsible for simulating a sensor that would monitor an individual spot. To demonstrate the real-world capability of this component, we create several processes, each one representing a simulator monitoring a parking space. The simulator performs a few key functions:

    - #### Simulating first-come first-serve drivers
        - Randomly and periodically sets the status of a parking space to "occupied/vacant" to resemble a driver pulling into the spot, then notifying the server that it status has changed
    - #### Processing reservations
        - Consuming messages published by the central server from the RabbitMQ server upon a reservation being made for that spot. Simulators only consume messages from the queue with the routing key matching their ID
        - Halting the random simulation process once it receives a reservation, and locally managing the reservation timing

- ### RabbitMQ Message Broker <a name="rabbit"></a>
    In order to facilitate communication between the server and the IoT simulators, it became clear that individual HTTP requests between 1 server and *n* simulators would lead to an unecessary amount of load. To deal with this, the server does not declare a queue, but instead uses a *routing key*, which is unique to a simulator node, to publish a message.

    Simulators are responsible for declaring their queues, and consuming from queues that match their routing key.

    This way, the server does not care what happens after that message is published. So long as it used the right routing key, it can continue its operation.

- ### Pricing Microservice <a name="pricing"></a>
    To alleviate load from the API server, and also avoid making calls to itself, we separated the dynamic pricing calculation into its own application. This service uses a timestamp, coupled with an analysis of the demand of the garage (data fetched from API) to calculate a *per-minute* rate. The benefits of separating this function are:

    - Less server load
    - No self calls by the server
    - Prevention of pricing injection from the client
        - Final reservation priced is only determined by this application. Although the client side can use this service to get pricing information, the final reservation creation is done by making a call to this service before being persisted to the database.

- ### Frontend Web UI <a name="ui"></a>
    Built once again in Python using the NiceGUI library, we created an interactive and user friendly way for drivers to interact with our application both on PC and mobile. This component features:
    - User signup and login
    - Overview of the garage availability
    - Reservation management


## Authors <a name="authors"></a>
- [Eric Muzzo](https://github.com/EricMuzzo)
    - [**Contact**](ericm02@me.com)
- Apisan Kaneshan
- Prevail Awoleye
- Digno Justin