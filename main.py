import sqlite3
import datetime


class DBOperations:
    """
    Handles all database operations such as table creation, CRUD actions,
    and SQL query execution for flights, pilots, destinations, and
    pilot assignments.
    """

    # SQL for creating each table
    # Create pilots table
    sql_create_pilots = """
    CREATE TABLE IF NOT EXISTS pilots (
        pilot_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        license_id TEXT UNIQUE NOT NULL,
        years_experience INTEGER
    )"""

    # Create destinations table
    sql_create_destinations = """
    CREATE TABLE IF NOT EXISTS destinations (
        destination_id INTEGER PRIMARY KEY,
        city TEXT NOT NULL,
        country TEXT NOT NULL,
        airport_code TEXT NOT NULL,
        UNIQUE(city, airport_code)
    )"""

    # Create flights table
    sql_create_flights = """
    CREATE TABLE IF NOT EXISTS flights (
        flight_id INTEGER PRIMARY KEY,
        flight_number TEXT NOT NULL,
        origin_id INTEGER NOT NULL,
        destination_id INTEGER NOT NULL,
        departure_time DATETIME NOT NULL,
        status TEXT DEFAULT 'Scheduled',
        FOREIGN KEY (origin_id) REFERENCES destinations(destination_id),
        FOREIGN KEY (destination_id) REFERENCES destinations(destination_id)
        CHECK (status IN ('Scheduled', 'Cancelled', 'Departed', 'Arrived', 'Delayed', 'Boarding', 'In Flight'))
        CHECK (origin_id <> destination_id)
    )"""

    # Create pilot assignments table
    sql_create_pilot_assignments = """
    CREATE TABLE IF NOT EXISTS pilot_assignments (
        assignment_id INTEGER PRIMARY KEY,
        flight_id INTEGER NOT NULL,
        pilot_id INTEGER NOT NULL,
        assignment_date DATETIME NOT NULL,
        FOREIGN KEY (flight_id) REFERENCES flights(flight_id),
        FOREIGN KEY (pilot_id) REFERENCES pilots(pilot_id),
        UNIQUE(flight_id, pilot_id)
    )"""

    # Sample data insertion
    sql_insert_pilot = (
        "INSERT INTO pilots (name, license_id, years_experience) VALUES (?, ?, ?)"
    )
    sql_insert_destination = (
        "INSERT INTO destinations (city, country, airport_code) VALUES (?, ?, ?)"
    )
    sql_insert_flight = "INSERT INTO flights (flight_number, origin_id, destination_id, departure_time, status) VALUES (?, ?, ?, ?, ?)"
    sql_insert_assignment = "INSERT INTO pilot_assignments (flight_id, pilot_id, assignment_date) VALUES (?, ?, ?)"

    def __init__(self):
        """
        Constructor function to establish the initial database connection and create all necessary tables.
        This method executes SQL commands to ensure that the pilots, destinations, flights, and pilot_assignments tables are created.
        """
        try:
            # Establish a connection to the database, saved as local file FlightManagement.db
            self.conn = sqlite3.connect("FlightManagement.db")
            self.cur = self.conn.cursor()

            # Create pilots, destinations, flights, and pilot_assignments tables
            self.cur.execute(self.sql_create_pilots)
            self.cur.execute(self.sql_create_destinations)
            self.cur.execute(self.sql_create_flights)
            self.cur.execute(self.sql_create_pilot_assignments)
            self.conn.commit()

            # Tables created succesffully

        except Exception as e:
            print(e)
        finally:
            # Close the connection after the tables are created
            # Subsequent database operations will open and close the connection as needed with get_connection()
            self.conn.close()

    def get_connection(self):
        """Establish a fresh connection to the database, making sure the database connection is active for each operation"""
        self.conn = sqlite3.connect("FlightManagement.db")
        self.cur = self.conn.cursor()

    def populate_sample_data(self):
        """Populate the database with sample data for each table, for testing and demonstration"""
        try:
            self.get_connection()

            # Sample pilot data
            pilots = [
                ("James Smith", "UK10001", 15),
                ("Jane Smith", "UK10002", 12),
                ("Michael Scott", "UK10003", 8),
                ("Tim Robinson", "UK10004", 20),
                ("Taylor Swift", "UK10005", 10),
                ("Matthew Fox", "UK10006", 7),
                ("John Locke", "UK10007", 5),
                ("Jim Halpert", "UK10008", 18),
                ("Adam Scott", "UK10009", 25),
                ("Travis Touchdown", "UK10010", 3),
                ("Sarah Connor", "UK10011", 22),
                ("Ellen Ripley", "UK10012", 19),
                ("Han Solo", "UK10013", 30),
                ("Cloud Strife", "UK10014", 15),
                ("Luke Skywalker", "UK10015", 12),
            ]

            # Insert sample pilot data
            for pilot in pilots:
                self.cur.execute(self.sql_insert_pilot, pilot)

            # Sample destination data
            destinations = [
                ("London", "UK", "LHR"),
                ("Tokyo", "Japan", "HND"),
                ("Seoul", "Korea", "KIX"),
                ("Paris", "France", "CDG"),
                ("Berlin", "Germany", "BER"),
                ("New York", "USA", "JFK"),
                ("Dubai", "UAE", "DXB"),
                ("Sydney", "Australia", "SYD"),
                ("Toronto", "Canada", "YYZ"),
                ("Los Angeles", "USA", "LAX"),
                ("Singapore", "Singapore", "SIN"),
                ("Hong Kong", "China", "HKG"),
                ("Rome", "Italy", "FCO"),
                ("Madrid", "Spain", "MAD"),
                ("Cape Town", "South Africa", "CPT"),
            ]

            # Insert sample destinations
            for destination in destinations:
                self.cur.execute(self.sql_insert_destination, destination)

            # Sample flight data
            flights = [
                ("BA101", 1, 2, "2025-03-10 10:00:00", "Scheduled"),
                ("BA102", 2, 1, "2025-03-10 14:00:00", "Scheduled"),
                ("BA103", 1, 3, "2025-03-11 09:00:00", "Scheduled"),
                ("BA104", 3, 4, "2025-03-12 12:00:00", "Scheduled"),
                ("BA105", 4, 5, "2025-03-13 15:00:00", "Scheduled"),
                ("BA106", 5, 6, "2025-03-14 08:00:00", "Scheduled"),
                ("BA107", 6, 7, "2025-03-15 11:00:00", "Scheduled"),
                ("BA108", 7, 8, "2025-03-16 13:00:00", "Scheduled"),
                ("BA109", 8, 9, "2025-03-17 16:00:00", "Scheduled"),
                ("BA110", 9, 10, "2025-03-18 18:00:00", "Scheduled"),
                ("BA111", 10, 11, "2025-03-19 07:00:00", "Scheduled"),
                ("BA112", 11, 12, "2025-03-20 09:00:00", "Scheduled"),
                ("BA113", 12, 13, "2025-03-21 11:00:00", "Scheduled"),
                ("BA114", 13, 14, "2025-03-22 13:00:00", "Scheduled"),
                ("BA115", 14, 15, "2025-03-23 15:00:00", "Scheduled"),
            ]

            # Insert flight data
            for flight in flights:
                self.cur.execute(self.sql_insert_flight, flight)

            # Sample pilot assignments (with multiple pilots per flight, e.g. copilots)
            assignments = [
                (1, 1, "2025-02-01 10:00:00"),  # Flight BA101, Pilot 1
                (1, 2, "2025-02-01 10:00:00"),  # Flight BA101, Pilot 2
                (2, 3, "2025-02-02 14:00:00"),  # Flight BA102, Pilot 3
                (3, 4, "2025-02-03 09:00:00"),  # Flight BA103, Pilot 4
                (3, 5, "2025-03-03 09:00:00"),  # Flight BA103, Pilot 5
                (4, 6, "2025-03-04 12:00:00"),  # Flight BA104, Pilot 6
                (5, 7, "2025-03-05 15:00:00"),  # Flight BA105, Pilot 7
                (6, 8, "2025-03-06 08:00:00"),  # Flight BA106, Pilot 8
                (7, 9, "2025-03-07 11:00:00"),  # Flight BA107, Pilot 9
                (8, 10, "2025-03-08 13:00:00"),  # Flight BA108, Pilot 10
                (8, 1, "2025-03-08 13:00:00"),  # Flight BA108, Pilot 1
                (9, 11, "2025-03-09 16:00:00"),  # Flight BA109, Pilot 11
                (10, 12, "2025-03-10 18:00:00"),  # Flight BA110, Pilot 12
                (11, 13, "2025-03-11 07:00:00"),  # Flight BA111, Pilot 13
                (12, 14, "2025-03-12 09:00:00"),  # Flight BA112, Pilot 14
                (12, 15, "2025-03-12 09:00:00"),  # Flight BA112, Pilot 15
            ]

            # Insert sample assignments
            for assignment in assignments:
                self.cur.execute(self.sql_insert_assignment, assignment)

            self.conn.commit()
            print("Sample data populated successfully")

        except Exception as e:
            print(f"Error populating sample data: {e}")
        finally:
            self.conn.close()

    def add_new_flight(self):
        """
        Adds a new flight to the database using flight details inputted by the user.
        Validates user input along the way.
        """
        try:
            self.get_connection()

            # Show available destinations
            print("\nAvailable Destinations:")
            self.cur.execute(
                "SELECT destination_id, city, country, airport_code FROM destinations"
            )
            destinations = self.cur.fetchall()
            for dest in destinations:
                print(f"ID: {dest[0]}. {dest[1]}, {dest[2]} (Code: {dest[3]})")

            # Get flight details
            flight_num = input("Enter Flight Number: ")
            origin_id = int(input("Enter Origin ID: "))
            dest_id = int(input("Enter Destination ID: "))
            departure = input("Enter Departure Time (YYYY-MM-DD HH:MM): ")
            # Validate the datetime input format before inserting
            try:
                # Parse the input string to a datetime object
                departure_dt = datetime.datetime.strptime(departure, "%Y-%m-%d %H:%M")
                # reformat to include seconds as required by SQLite
                departure = departure_dt.strftime("%Y-%m-%d %H:%M:%S")
            except ValueError:
                print("Invalid datetime format. Please use 'YYYY-MM-DD HH:MM'")
                # Exit method so that invalid data isn't inserted
                return

            # Insert flight to DB
            self.cur.execute(
                self.sql_insert_flight,
                (flight_num, origin_id, dest_id, departure, "Scheduled"),
            )

            self.conn.commit()
            print("Flight added successfully")

        except Exception as e:
            print(f"Error adding flight: {e}")
        finally:
            self.conn.close()

    def view_flights_by_criteria(self):
        """Present a menu to search for flights by destination, status, or date."""
        try:
            self.get_connection()
            print("\nSearch by:")
            print("1. Destination")
            print("2. Status")
            print("3. Date")
            print("4. All")
            choice = int(input("Enter choice: "))

            if choice == 1:
                # Search by destination city name
                dest = input("Enter destination city name: ")
                query = """
                SELECT f.flight_number, d1.city as Origin, d2.city as Destination, 
                       f.departure_time, f.status
                FROM flights f
                JOIN destinations d1 ON f.origin_id = d1.destination_id
                JOIN destinations d2 ON f.destination_id = d2.destination_id
                WHERE d2.city LIKE ?
                """
                self.cur.execute(query, (f"%{dest}%",))

            elif choice == 2:
                # Search by flight status (e.g. Scheduled, Cancelled, etc)
                status = input("Enter status: ")
                query = """
                SELECT f.flight_number, d1.city as Origin, d2.city as Destination, 
                       f.departure_time, f.status
                FROM flights f
                JOIN destinations d1 ON f.origin_id = d1.destination_id
                JOIN destinations d2 ON f.destination_id = d2.destination_id
                WHERE f.status LIKE ?
                """
                self.cur.execute(query, (f"%{status}%",))

            elif choice == 3:
                # Search by date (YYYY-MM-DD)
                date = input("Enter date (YYYY-MM-DD): ")
                query = """
                SELECT f.flight_number, d1.city as Origin, d2.city as Destination, 
                       f.departure_time, f.status
                FROM flights f
                JOIN destinations d1 ON f.origin_id = d1.destination_id
                JOIN destinations d2 ON f.destination_id = d2.destination_id
                WHERE DATE(f.departure_time) = ?
                """
                self.cur.execute(query, (date,))

            elif choice == 4:
                # Return all flights to the user
                query = """
                SELECT f.flight_number, d1.city as Origin, d2.city as Destination, 
                    f.departure_time, f.status
                FROM flights f
                JOIN destinations d1 ON f.origin_id = d1.destination_id
                JOIN destinations d2 ON f.destination_id = d2.destination_id
                """
                self.cur.execute(query)

            else:
                print("Invalid choice. Please select a valid option.")
                return

            results = self.cur.fetchall()
            if results:
                # Print the results table for each flight
                for row in results:
                    print(f"\nFlight Number: {row[0]}")
                    print(f"Route: {row[1]} -> {row[2]}")
                    print(f"Departure: {row[3]}")
                    print(f"Status: {row[4]}")
            else:
                print("No flights found matching criteria")

        except Exception as e:
            print(f"Error viewing flights: {e}")
        finally:
            self.conn.close()

    def update_flight_info(self):
        """Present options to update specific flight information: departure time or status."""
        try:
            self.get_connection()
            flight_num = input("Enter Flight Number to update: ")

            print("\nWhat would you like to update?")
            print("1. Departure Time")
            print("2. Status")
            choice = int(input("Enter choice: "))

            if choice == 1:
                new_time = input("Enter new departure time (YYYY-MM-DD HH:MM): ")
                try:
                    new_time_dt = datetime.datetime.strptime(new_time, "%Y-%m-%d %H:%M")
                    new_time = new_time_dt.strftime("%Y-%m-%d %H:%M:%S")
                except ValueError:
                    print("Invalid datetime format. Please use 'YYYY-MM-DD HH:MM'")
                    return
                self.cur.execute(
                    """
                    UPDATE flights 
                    SET departure_time = ? 
                    WHERE flight_number = ?
                """,
                    (new_time, flight_num),
                )

            elif choice == 2:
                new_status = input("Enter new status: ")
                self.cur.execute(
                    """
                    UPDATE flights 
                    SET status = ? 
                    WHERE flight_number = ?
                """,
                    (new_status, flight_num),
                )

            if self.cur.rowcount > 0:
                self.conn.commit()
                print("Flight updated successfully")
            else:
                print("Flight not found")

        except Exception as e:
            print(f"Error updating flight: {e}")
        finally:
            self.conn.close()

    def validate_flight_id_exists(self, flight_id):
        """Check if a flight exists in the database."""
        self.get_connection()
        self.cur.execute(
            "SELECT flight_id FROM flights WHERE flight_id = ?", (flight_id,)
        )
        return self.cur.fetchone() is not None

    def validate_pilot_exists(self, pilot_id):
        """Check if a pilot exists in the database."""
        self.get_connection()
        self.cur.execute("SELECT pilot_id FROM pilots WHERE pilot_id = ?", (pilot_id,))
        return self.cur.fetchone() is not None

    def assign_pilot(self):
        """Create a new assignment for a pilot to a specific flight."""
        try:
            self.get_connection()

            # Show available flights
            print("\nAvailable Flights:")
            self.cur.execute(
                """
                SELECT f.flight_id, f.flight_number, d1.city as Origin, d2.city as Destination
                FROM flights f
                JOIN destinations d1 ON f.origin_id = d1.destination_id
                JOIN destinations d2 ON f.destination_id = d2.destination_id
                WHERE f.departure_time > datetime('now')
            """
            )
            flights = self.cur.fetchall()
            for flight in flights:
                print(f"{flight[0]}. {flight[1]} ({flight[2]} -> {flight[3]})")

            # Show available pilots
            print("\nAvailable Pilots:")
            self.cur.execute("SELECT pilot_id, name, years_experience FROM pilots")
            pilots = self.cur.fetchall()
            for pilot in pilots:
                print(f"{pilot[0]}. {pilot[1]} (Experience: {pilot[2]} years)")

            flight_id = int(input("\nEnter Flight ID: "))

            # Validate flight exists
            if not self.validate_flight_id_exists(flight_id):
                print(f"Error: Flight with ID {flight_id} does not exist")
                return

            pilot_id = int(input("Enter Pilot ID: "))

            # Validate pilot exists
            if not self.validate_pilot_exists(pilot_id):
                print(f"Error: Pilot with ID {pilot_id} does not exist")
                return

            assignment_date = input(
                "Enter Assignment Date (YYYY-MM-DD HH:MM) [Leave blank for current date/time]: "
            ).strip()

            if assignment_date == "":
                # Use the current date/time if no date/time was provided
                assignment_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            else:
                try:
                    assignment_dt = datetime.datetime.strptime(
                        assignment_date, "%Y-%m-%d %H:%M"
                    )
                    assignment_date = assignment_dt.strftime("%Y-%m-%d %H:%M:%S")
                except ValueError:
                    print("Invalid datetime format. Please use 'YYYY-MM-DD HH:MM'")
                    return

            self.cur.execute(
                self.sql_insert_assignment, (flight_id, pilot_id, assignment_date)
            )
            self.conn.commit()
            print("Pilot assigned successfully")

        except Exception as e:
            print(f"Error assigning pilot: {e}")
        finally:
            self.conn.close()

    def view_pilot_schedule(self):
        """View the schedule of a pilot based on their ID."""
        try:
            self.get_connection()
            pilot_id = input("Enter Pilot ID: ")

            query = """
            SELECT p.name, f.flight_number, d1.city as Origin, d2.city as Destination,
                   f.departure_time, pa.assignment_date
            FROM pilots p
            JOIN pilot_assignments pa ON p.pilot_id = pa.pilot_id
            JOIN flights f ON pa.flight_id = f.flight_id
            JOIN destinations d1 ON f.origin_id = d1.destination_id
            JOIN destinations d2 ON f.destination_id = d2.destination_id
            WHERE p.pilot_id = ?
            ORDER BY f.departure_time
            """

            self.cur.execute(query, (pilot_id,))
            schedule = self.cur.fetchall()

            if schedule:
                print(f"\nSchedule for {schedule[0][0]}:")
                for flight in schedule:
                    print(f"\nFlight: {flight[1]}")
                    print(f"Route: {flight[2]} -> {flight[3]}")
                    print(f"Departure: {flight[4]}")
                    print(f"Assignment Date: {flight[5]}")
            else:
                print("No flights scheduled for this pilot")

        except Exception as e:
            print(f"Error viewing schedule: {e}")
        finally:
            self.conn.close()

    def manage_destinations(self):
        """View, add, and update destinations by using the defined options."""
        try:
            self.get_connection()
            print("\nDestination Management:")
            print("1. View all destinations")
            print("2. Add new destination")
            print("3. Update destination")
            choice = int(input("Enter choice: "))

            if choice == 1:
                self.cur.execute("SELECT * FROM destinations")
                destinations = self.cur.fetchall()
                for dest in destinations:
                    print(f"\nID: {dest[0]}")
                    print(f"City: {dest[1]}")
                    print(f"Country: {dest[2]}")
                    print(f"Airport Code: {dest[3]}")

            elif choice == 2:
                city = input("Enter city: ")
                country = input("Enter country: ")
                airport_code = input("Enter airport code: ")
                self.cur.execute(
                    self.sql_insert_destination, (city, country, airport_code)
                )
                self.conn.commit()
                print("Destination added successfully")

            elif choice == 3:
                dest_id = input("Enter Destination ID to update: ")
                city = input("Enter new city (or press enter to skip): ")
                country = input("Enter new country (or press enter to skip): ")
                airport_code = input(
                    "Enter new airport code (or press enter to skip): "
                )

                updates = []
                values = []
                if city:
                    updates.append("city = ?")
                    values.append(city)
                if country:
                    updates.append("country = ?")
                    values.append(country)
                if airport_code:
                    updates.append("airport_code = ?")
                    values.append(airport_code)

                if updates:
                    values.append(dest_id)
                    query = f"UPDATE destinations SET {', '.join(updates)} WHERE destination_id = ?"
                    self.cur.execute(query, tuple(values))
                    self.conn.commit()
                    print("Destination updated successfully")

        except Exception as e:
            print(f"Error managing destinations: {e}")
        finally:
            self.conn.close()

    def delete_flight(self):
        """Delete a flight based on Flight Number."""
        try:
            self.get_connection()
            flight_num = input("Enter Flight Number to delete: ")
            self.cur.execute(
                "DELETE FROM flights WHERE flight_number = ?", (flight_num,)
            )
            if self.cur.rowcount > 0:
                self.conn.commit()
                print("Flight deleted successfully")
            else:
                print("Flight not found")
        except Exception as e:
            print(f"Error deleting flight: {e}")
        finally:
            self.conn.close()

    def summarise_flights_by_destination(self):
        """Show number of flights per destination."""
        try:
            self.get_connection()

            # SQL query to count flights by destination
            query = """
            SELECT d.city, COUNT(f.flight_id) as flight_count
            FROM flights f
            JOIN destinations AS d ON f.destination_id = d.destination_id
            GROUP BY d.city
            """
            self.cur.execute(query)
            results = self.cur.fetchall()

            print("\nFlight Counts by Destination:")
            # Print into table
            for row in results:
                print(f"Destination: {row[0]}: {row[1]} flight(s)")
        except Exception as e:
            print(f"Error summarising flights: {e}")
        finally:
            self.conn.close()

    def get_pilot_flight_count(self):
        """Get a summary of flights assigned to each pilot."""
        try:
            self.get_connection()
            query = """
            SELECT
                p.pilot_id,
                p.name,
                p.license_id,
                COUNT(pa.flight_id) as flight_count,
                COUNT(CASE WHEN f.departure_time > datetime('now') THEN 1 END) as upcoming_flights
            FROM pilots p
            LEFT JOIN pilot_assignments pa ON p.pilot_id = pa.pilot_id
            LEFT JOIN flights f ON pa.flight_id = f.flight_id
            GROUP BY p.pilot_id, p.name, p.license_id
            ORDER BY flight_count DESC
            """
            self.cur.execute(query)
            results = self.cur.fetchall()

            print("\nPilot Flight Assignments Summary:")
            print("-----------------")
            for row in results:
                print(f"Pilot ID: {row[0]}")
                print(f"Pilot: {row[1]} (License: {row[2]})")
                print(f"Total Flights: {row[3]}")
                print(f"Upcoming Flights: {row[4]}")
                print("-----------------")

        except Exception as e:
            print(f"Error getting pilot flight count: {e}")
        finally:
            self.conn.close()

    def get_destination_statistics(self):
        """Get comprehensive statistics about destinations."""
        try:
            self.get_connection()
            query = """
            SELECT 
                d.city,
                d.country,
                COUNT(f.flight_id) as total_flights,
                COUNT(DISTINCT p.pilot_id) as unique_pilots,
                COUNT(CASE WHEN f.status = 'Delayed' THEN 1 END) as delayed_flights,
                COUNT(CASE WHEN f.status = 'Cancelled' THEN 1 END) as cancelled_flights
            FROM destinations d
            LEFT JOIN flights f ON d.destination_id = f.destination_id
            LEFT JOIN pilot_assignments pa ON f.flight_id = pa.flight_id
            LEFT JOIN pilots p ON pa.pilot_id = p.pilot_id
            GROUP BY d.city, d.country
            ORDER BY total_flights DESC
            """
            self.cur.execute(query)
            results = self.cur.fetchall()

            print("\nDestination Statistics:")
            for row in results:
                print(f"\nDestination: {row[0]}, {row[1]}")
                print(f"Total Flights: {row[2]}")
                print(f"Unique Pilot Count: {row[3]}")
                print(f"Delayed Flights: {row[4]}")
                print(f"Cancelled Flights: {row[5]}")

        except Exception as e:
            print(f"Error getting destination statistics: {e}")
        finally:
            self.conn.close()

    def delete_pilot_assignment(self):
        """Delete a pilot assignment."""
        try:
            self.get_connection()
            assignment_id = input("Enter Assignment ID to delete: ")
            self.cur.execute(
                "DELETE FROM pilot_assignments WHERE assignment_id = ?",
                (assignment_id,),
            )
            if self.cur.rowcount > 0:
                self.conn.commit()
                print("Assignment deleted successfully")
            else:
                print("Assignment not found")

        except Exception as e:
            print(f"Error managing assignments: {e}")
        finally:
            self.conn.close()

    def manage_pilots(self):
        """View, add, update, or delete pilots."""
        try:
            self.get_connection()
            print("\nPilot Management:")
            print("1. View all pilots")
            print("2. Add a new pilot")
            print("3. Update a pilot")
            print("4. Delete a pilot")
            choice = int(input("Enter choice: "))

            if choice == 1:
                self.cur.execute("SELECT * FROM pilots")
                pilots = self.cur.fetchall()
                for pilot in pilots:
                    print(f"\nID: {pilot[0]}")
                    print(f"Name: {pilot[1]}")
                    print(f"License ID: {pilot[2]}")
                    print(f"Years Experience: {pilot[3]}")

            elif choice == 2:
                name = input("Enter pilot name: ")
                license_id = input("Enter license ID: ")
                years_exp = int(input("Enter years of experience: "))
                self.cur.execute(self.sql_insert_pilot, (name, license_id, years_exp))
                self.conn.commit()
                print("Pilot added successfully")

            elif choice == 3:
                pilot_id = input("Enter Pilot ID to update: ")
                name = input("Enter new name (or press enter to skip): ")
                license_id = input("Enter new license ID (or press enter to skip): ")
                years_exp = input(
                    "Enter new years of experience (or press enter to skip): "
                )

                updates = []
                values = []

                if name:
                    updates.append("name = ?")
                    values.append(name)
                if license_id:
                    updates.append("license_id = ?")
                    values.append(license_id)
                if years_exp:
                    updates.append("years_experience = ?")
                    values.append(int(years_exp))

                # only try to update if one or more fields have changed
                if updates:
                    # add pilot_id for the WHERE clause at the end
                    values.append(pilot_id)

                    # dynamically build the query for each column needed to update
                    query = f"UPDATE pilots SET {', '.join(updates)} WHERE pilot_id = ?"

                    # execute query with all values
                    self.cur.execute(query, tuple(values))
                    self.conn.commit()
                    print("Pilot updated successfully")

            elif choice == 4:
                pilot_id = input("Enter Pilot ID to delete: ")

                # First check if the pilot has any assignments
                self.cur.execute(
                    "SELECT COUNT(*) FROM pilot_assignments WHERE pilot_id = ?",
                    (pilot_id,),
                )
                assignment_count = self.cur.fetchone()[0]

                if assignment_count > 0:
                    print(
                        f"Can not delete pilot as they have {assignment_count} flight assignments. Delete these assignments first."
                    )
                    return

                self.cur.execute("DELETE FROM pilots WHERE pilot_id = ?", (pilot_id,))
                if self.cur.rowcount > 0:
                    self.conn.commit()
                    print("Pilot deleted successfully")
                else:
                    print("Pilot not found")

        except Exception as e:
            print(f"Error managing pilots: {e}")
        finally:
            self.conn.close()


# The main function will parse arguments.
# These argument will be defined by the users on the console.
# The user will select a choice from the menu to interact with the database.

# This menu allows the user to manage flights, pilots, and destinations.
while True:
    print("\n Menu:")
    print("**********")
    print(" 1. Add a New Flight")
    print(" 2. View Flights by Criteria")
    print(" 3. Update Flight Information")
    print(" 4. Assign Pilot to Flight")
    print(" 5. View Pilot Schedule")
    print(" 6. View/Update Destination Information")
    print(" 7. Delete a Flight")
    print(" 8. Summarise Flights by Destination")
    print(" 9. View Pilot Flight Summary")
    print(" 10. View Destination Statistics")
    print(" 11. Manage a Pilot")
    print(" 12. Delete a Pilot Assignment")
    print(" 13. Populate Sample Data")
    print(" 14. Exit\n")

    try:
        __choose_menu = int(input("Enter your choice: "))
        db_ops = DBOperations()

        if __choose_menu == 1:
            db_ops.add_new_flight()
        elif __choose_menu == 2:
            db_ops.view_flights_by_criteria()
        elif __choose_menu == 3:
            db_ops.update_flight_info()
        elif __choose_menu == 4:
            db_ops.assign_pilot()
        elif __choose_menu == 5:
            db_ops.view_pilot_schedule()
        elif __choose_menu == 6:
            db_ops.manage_destinations()
        elif __choose_menu == 7:
            db_ops.delete_flight()
        elif __choose_menu == 8:
            db_ops.summarise_flights_by_destination()
        elif __choose_menu == 9:
            db_ops.get_pilot_flight_count()
        elif __choose_menu == 10:
            db_ops.get_destination_statistics()
        elif __choose_menu == 11:
            db_ops.manage_pilots()
        elif __choose_menu == 12:
            db_ops.delete_pilot_assignment()
        elif __choose_menu == 13:
            db_ops.populate_sample_data()
        elif __choose_menu == 14:
            exit(0)
        else:
            print("Invalid Choice")
    except ValueError:
        print("Please enter a valid number")
    except Exception as e:
        print(f"An error occurred: {e}")
