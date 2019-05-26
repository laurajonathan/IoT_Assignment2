"""
reception_main.py

Created by  Suwat Tangtragoonviwatt (s3710374)
            Laura Jonathan (s3696013)
            Warren Shipp (s3690682)
            Aidan Afonso (s3660805)

This script is intended to run the smart library system as a reception device

"""

import re
import socket
import getpass
import MySQLdb
from passlib.hash import sha256_crypt
from qr_code_scanner import QRCodeScanner
from facial_recognition import Capture, Trainer, Recogniser
from voice_recognition import VoiceRecognition

PORT = 65000  # The port used by the server.
BUFFER = 4096


class DatabaseReception:
    """
    Database class for all local database operations
    """

    def __init__(self, connection=None):
        if connection is None:
            connection = MySQLdb.connect(
                "localhost", "pi", "suwat513", "Assignment2"
            )
        self.__connection = connection

    def __execute_query(self, query, *attributes):
        """
        Execute query
        """
        with self.__connection.cursor() as cursor:
            cursor.execute(query, attributes)
            result = cursor.fetchall()
        self.__connection.commit()
        return result

    @classmethod
    def __validate_data(cls, *attributes):
        """
        Validate the type of the data before insert into database
        """
        for attr in attributes:
            if not isinstance(attr, str):
                return False
        return True

    def insert_data(self, *attributes):
        """
        Validate the data and prevent SQL Injection attack with
        parametrised query then insert data into database
        """
        query = """
            INSERT INTO users (
                username,
                password,
                firstname,
                lastname,
                email,
                type
                ) VALUES (%s, %s, %s, %s, %s, %s)
        """
        if self.__validate_data(*attributes):
            self.__execute_query(query, *attributes)

    def read_data(self, username):
        """
        Read data from the database with pre-defined query
        """
        query = """
            SELECT username, password
            FROM users
            WHERE username = '{}'
        """.format(username)
        return self.__execute_query(query)

    def __del__(self):
        self.__connection.close()


class NetworkReception():
    """
    Network class to communicate between device (RP and MP)
    """
    def __init__(self, address, buffer=BUFFER):
        self.address = address
        self.buffer = buffer

    def manage(self):
        """
        Manage something
        """

    def run(self, username):
        """
        Run
        """
        # Connect to Master PI
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
            print("Connecting to {}...".format(self.address))
            soc.connect(self.address)
            # Send username to establish communication
            soc.sendall(username.encode())
            # Wait for confirmation message
            data = soc.recv(self.buffer)
            print(data.decode())
            if data.decode() == "Success!":
                # Wait for welcome message and menu
                data = soc.recv(self.buffer)
                print(data.decode())
                # Start communication
                while True:
                    # Prompt for user input
                    message = input("Master PI: $ ")
                    # Send message
                    soc.sendall(message.encode())
                    # Wait for response
                    data = soc.recv(self.buffer)
                    # Check if Disconnected from Master Pi
                    if data.decode() == "Disconnect!":
                        break
                    # Check if it a submenu
                    if data.decode() == "submenu":
                        self.run_submenu(soc, "")
                    else:
                        # Print out to console
                        print(data.decode())
                print("Disconnecting from server.")
            else:
                # Handshake authentication failed
                soc.sendall("Disconnect!".encode())
        print("Disconnected")

    def run_submenu(self, soc, sub_menu):
        """
        Run Submenu
        """
        # Wait for response
        data = soc.recv(self.buffer)
        # Print out to console
        print(data.decode())
        sub_menu = sub_menu + "/" + data.decode().strip().split(" ")[0]
        # Run QR Code Scanner
        if sub_menu == "/Return/QR":
            qr_code_scanner = QRCodeScanner()
            qr_code_scanner.setup()
            message = qr_code_scanner.run()
            del qr_code_scanner
        elif sub_menu == "/Search/Voice":
            # Run Voice Recognition
            voice_recognition = VoiceRecognition()
            error_message, message = voice_recognition.listen()
            if error_message:
                message = ""
                print(error_message)
        else:
            # Prompt for user input
            message = input("Master PI:{} $ ".format(sub_menu))
        # Send message
        soc.sendall(message.encode())
        # Wait for response
        data = soc.recv(self.buffer)
        # Check if it a submenu
        if data.decode() == "submenu":
            self.run_submenu(soc, sub_menu)
        else:
            # Print out to console
            print(data.decode())


class Reception():
    """
    Reception PI
    """
    def __init__(self, database=DatabaseReception()):
        self.database = database

    @classmethod
    def __read_input(cls, message, regex, limit=2):
        """
        Read user input from console and validate according to regex set
        """
        # Invalid input count
        count = 0
        if message == "password":
            # Password Input
            prompt_msg = "Input password: "
            password = getpass.getpass(prompt=prompt_msg)
            # Remove all write space and newline from regex
            regex = regex.replace("\n", "").replace(" ", "")
            # Password validation
            while not re.match(regex, password) and count <= limit:
                # Invalid input limit reached
                if count >= limit:
                    return ""
                print("Regex - {}".format(regex))
                print("Invalid Input!", (limit - count))
                password = getpass.getpass(prompt=prompt_msg)
                count += 1

            # Re-input password validation
            count = 0
            prompt_msg = "Input password again: "
            value = getpass.getpass(prompt=prompt_msg)
            while value != password and count <= limit:
                # Invalid input limit reached
                if count >= limit:
                    return ""
                print("Same as previous input")
                print("Invalid Input!", (limit - count))
                value = getpass.getpass(prompt=prompt_msg)
                count += 1
        else:
            # Other Input validation
            value = input("Input " + message + ": ")
            while not re.match(regex, value) and count <= limit:
                # Invalid input limit reached
                if count >= limit:
                    return ""
                print("Regex - {}".format(regex))
                print("Invalid Input!", (limit - count))
                print(count, limit)
                value = input("Input " + message + " again: ")
                count += 1

        return value

    def register(self):
        """
        Register interface and logic
        """
        # Welcome message
        print("Welcome!")
        print("Please input user detail")
        # Read username
        username = self.__read_input("username", r"^(?=.{8,20}$)[\w]+$")
        if not username:
            return False
        # Read password
        password = self.__read_input(
            "password",
            r"""
                ^(?=.*[a-z])
                (?=.*[A-Z])
                (?=.*\d)
                (?=.*[@$!%*#?&])
                [A-Za-z\d@$!#%*?&]{6,20}$
            """
        )
        if not password:
            return False
        # Read firstname
        firstname = self.__read_input("first name", r"[A-Za-z]+$")
        if not firstname:
            return False
        # Read lastname
        lastname = self.__read_input("last name", r"[A-Za-z]+$")
        if not lastname:
            return False
        # Read email address
        email = self.__read_input("email address", r"[^@]+@[^@]+\.[^@]+")
        if not email:
            return False

        # Hash the password
        hashed_password = sha256_crypt.hash(password)

        # Update database detail
        self.database.insert_data(
            username,
            hashed_password,
            firstname,
            lastname,
            email,
            "user"
        )
        return True

    def login(self):
        """
        Login interface and logic
        """
        # Read input from user
        username = input("Enter username: ")
        password = getpass.getpass(prompt="Enter password: ")
        # Get username and password from database
        data = self.database.read_data(username)
        if data:
            user_db, pass_db = data[0]
            if (username == user_db
                    and sha256_crypt.verify(password, pass_db)):
                return username
        return ""

    def register_by_facial_recognition(self):
        """
        Register by facial recognition interface and logic
        """
        # Welcome message
        print("Welcome!")
        print("Please input user detail")
        # Read username
        username = self.__read_input("username", r"^(?=.{8,20}$)[\w]+$")
        if not username:
            return False

        # Start capture the image
        capture = Capture(username)
        capture.configure()
        capture.run()
        del capture

        # Train the image
        trainer = Trainer()
        trainer.run()
        trainer.save()

        return True

    @classmethod
    def login_by_facial_recognition(cls):
        """
        Login by facial recognition interface and logic
        """
        recogniser = Recogniser()
        recogniser.load()
        username = recogniser.run()
        del recogniser

        if username:
            return username
        return ""

    @classmethod
    def menu(cls):
        """
        Menu interface for register or login
        """
        menu = """
            Menu
            (1) Register
            (2) Register with Facial Recognition
            (3) Login
            (4) Login with Facial Recognition
            (enter) Exit
        """
        print(menu)
        option = input("Input Option: ")
        while option not in ("1", "2", "3", "4", ""):
            print("Invalid Input!")
            print(menu)
            option = input("Input Option Again: ")

        return option

    def __del__(self):
        del self.database


def main():
    """
    Main Method
    """
    # Initialization
    host = input("Enter IP address of Master PI: ")
    address = (host, PORT)
    reception = Reception()
    network = NetworkReception(address)
    # Run menu
    while True:
        option = reception.menu()
        # Login
        if option in ("3", "4"):
            if option == "3":
                username = reception.login()
            else:
                username = reception.login_by_facial_recognition()
            # Login successful
            if username:
                # Run socket communication to Master PI
                network.run(username)
            else:
                print("Login Failed!")
        # Register
        elif option in ("1", "2"):
            if option == "1":
                result = reception.register()
            else:
                result = reception.register_by_facial_recognition()
            if result:
                print("Registration Success!")
            else:
                print("Registration Failed!")
        else:
            print("Goodbye")
            break
    # Close database connection
    del reception


if __name__ == "__main__":
    main()
