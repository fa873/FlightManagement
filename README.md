# Flight Management

This Python application was built to manage flights, pilots, and destinations for an airline company. This is achieved using a command-line interface to perform CRUD operations on an SQLite database storing relevant data.

## Running the application

- Running `main.py` with Python will start the application in the terminal
- The user is presented with options selected by entering an integer
- The `FlightManagement.db` file is pre-populated with sample data
- If `FlightManagement.db` is deleted, it can be re-populated with sample data by selecting the `Populate Sample Data` option in the menu
- If `FlightManagement.db` already exists, the `Populate Sample Data` option will fail due to certain data already existing in the database.

## Features

The following options are available to the user on the menu:
- Add a New Flight
- View Flights by Criteria
- Update Flight Information
- Assign Pilot to Flight
- View Pilot Schedule
- View/Update Destination Information
- Delete a Flight
- Summarise Flights by Destination
- View Pilot Flight Summary
- View Destination Statistics
- Manage a Pilot
- Delete a Pilot Assignment
- Populate Sample Data
- Exit
