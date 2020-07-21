import mysql.connector

class MyDB:
    def __init__(self):
        db_name = "abdullah_assignment2"
        db_user = "root"
        db_pass = "LasithMalinga4w"
        db_host = "localhost"

        print("Connecting to database")
        self.conn = mysql.connector.connect(user=db_user, password=db_pass, host=db_host)
        cursor = self.conn.cursor()
        try:
            cursor.execute(f"USE {db_name};")
        except mysql.connector.errors.ProgrammingError as err:
            if err.args[2] == "42000":
                cursor.execute(f"CREATE DATABASE {db_name};")
                cursor.execute(f"USE {db_name};")

        try:
            cursor.execute("""CREATE TABLE dailygeneration
                        (date DATE NOT NULL PRIMARY KEY,
                        power_generation FLOAT(9,2)
                        );""")
        except mysql.connector.errors.ProgrammingError as err:
            if err.args[2] != "42S01":
                print(err.args)

        try:
            cursor.execute("""CREATE TABLE dailyerror
                        (id INT AUTO_INCREMENT PRIMARY KEY,
                        dev_name VARCHAR(255),
                        name VARCHAR(255),
                        inv_name VARCHAR(255),
                        alarm_id VARCHAR(255),
                        date_time DATETIME,
                        clear_time DATETIME,
                        alarm_msg VARCHAR(255)
                        );""")
        except mysql.connector.errors.ProgrammingError as err:
            if err.args[2] != "42S01":
                print(err.args)

    def get_instance(self):
        return self.conn

    def __del__(self):
        #Closing the connection
        print("Database connection closed")
        self.conn.close()
