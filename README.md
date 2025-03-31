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