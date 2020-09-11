# ISYS2120 Assignment 3 Documentation

## About
This is a web application designed for user device management. This webapp allows for users to view their devices and allows managers to issue and revoke the devices. Dummy data is provided to allow for you to navigate through the web application and understand what data is used and how it is used.

### Please Note
There will most definitely be bugs. Most of the bugs will occur when no values are returned from the database or the list is handled inappropriately. The main files for the bugs will be database.py and routes.py.

## Source code

### Main Important Files :

#### config.ini
- Edit this to have your database connection information
- user = your PgAdmin login username
- password = password for pgAdmin

#### database.py 
- Sets up connections to the database
- Runs all the SQL queries (you write)
- Has all the database functions

#### routes.py
- Handles how the website runs.
- Provides the routes (e.g. website.com/myroute )

## Manager Adding/Removing devices

### Adding
- To add a device, go to "issue device".
- Select an employee from the list
- Select a model and manufacturer
    - NOTE: this sends a request to the database to get the device models that have not yet been assigned.
- Select the device_id and press "Issue Device".
- If successful, you will see a "green" bar and show success.

### Removing
- Go to "manage department"
- Select a model/manufacturer
- Select an employee
- Click the red circle next to the device.
- If successful, you will see a "green" bar.
