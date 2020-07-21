# Scraping-Solar-Data
Scraping data from a solar website

## HOW TO USE
1. Enter database name, user, password, and host in create_db.py
2. Run assignment.py

## create_db.py
Create database and tables if not already created and creates a connection with the database. 
**get_instance** method returns the connection object. 
**Destructor** closes the connection.

## myhttp.py
The motivation was to separate the meta data of the requests from the scraping logic. 
**get_token** method gets authorization token for making the subsequent authorized requests.
**send_request** method sent the request to the given end point by adding the headers and the given payload to the request.

## assignment.py
Here we collect the required data and store it in the database.
**get_daily_generation_data** method returns the daily generation data of the given month and year.
**get_error_data** method gets the error data between the given start_date and end_date.
