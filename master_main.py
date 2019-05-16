"""
reception_main.py

Created by  Suwat Tangtragoonviwatt (s3710374)
            Laura Jonathan (s3696013)
            Warren Shipp (s3690682)
            Aidan Afonso (s3660805)

This script is intended to .....

"""

import datetime
import socket
import MySQLdb

HOST = ""  # Empty string means to listen on all IP's on the machine.
PORT = 65000  # Port to listen on (non-privileged ports are > 1023).
ADDRESS = (HOST, PORT)
BUFFER = 4096


class Database:
    """
    Database class for all local database operations
    """

    def __init__(self):
        self.__connection = MySQLdb.connect(
            "35.197.173.114", "root", "suwat513", "Assignment2"
        )

    def __execute_cloud_query(self, cloud_query, *attributes):
        """
        Execute query
        """
        with self.__connection.cursor() as cursor:
            cursor.execute(cloud_query, attributes)
            result = cursor.fetchall()
        self.__connection.commit()
        return result

    @classmethod
    def __validate_user(cls, *attributes):
        """
        Validate the type of the data before insert into cloud database
        """
        for attr in attributes:
            if not isinstance(attr, str):
                return False
        return True

    @classmethod
    def __validate_record(cls, *attributes):
        """
        Validate the type of the data before insert into cloud database
        """
        for attr in attributes:
            if isinstance(attr, str):
                if attr != "borrowed" and attr != "returned":
                    return False
        return True

    def insert_record(self, *attributes):
        """
        Validate the data and prevent SQL Injection attack with
        parametrised query then insert data into database
        """
        query = """
            INSERT INTO Record (
                UserID,
                BookID,
                Status,
                Quantity,
                BorrowedDate
                ) VALUES (%s, %s, %s, %s, %s)
        """
        if self.__validate_record(*attributes):
            self.__execute_cloud_query(query, *attributes)

    def insert_user(self, username):
        """
        Validate the data and prevent SQL Injection attack with
        parametrised query then insert data into database
        """
        query = """
            INSERT INTO User (Username) VALUES (%s)
        """
        if self.__validate_user(username):
            self.__execute_cloud_query(query, username)

    def get_user_id(self, username):
        """
        Get UserID from the database with pre-defined query
        """
        query = """
            SELECT UserID FROM User WHERE Username = '{}'
        """.format(username)
        return self.__execute_cloud_query(query)

    def get_book_id(self, title="", author="", isbn=""):
        """
        Get BookID from the database with pre-defined query
        """
        query = """
            SELECT BookID FROM Book
            WHERE Title = '{}'
            OR Author = '{}'
            OR ISBN = '{}'
        """.format(title, author, isbn)
        return self.__execute_cloud_query(query)

    def read_user(self, username):
        """
        Read user from the database with pre-defined query
        """
        query = """
            SELECT * FROM User WHERE Username = '{}'
        """.format(username)
        return self.__execute_cloud_query(query)

    def read_book(self, title="", author="", isbn=""):
        """
        Read book from the database with pre-defined query
        """
        query = """
            SELECT * FROM Book
            WHERE Title = '{}'
            OR Author = '{}'
            OR ISBN = '{}'
        """.format(title, author, isbn)
        return self.__execute_cloud_query(query)

    def read_book_from_id(self, book_id):
        """
        Read book from id from the database with pre-defined query
        """
        query = """
            SELECT Title, ISBN, Quantity FROM Book
            WHERE BookID = '{}'
        """.format(book_id)
        return self.__execute_cloud_query(query)

    def read_all_book(self):
        """
        Read all book from the database with pre-defined query
        """
        query = """
            SELECT * FROM Book
        """
        return self.__execute_cloud_query(query)

    def read_borrowed_record(self, user_id):
        """
        Read record from the database with pre-defined query
        """
        query = """
            SELECT RecordID, BookID, BorrowedDate FROM Record
            WHERE UserID = '{}'
            AND Status = 'borrowed'
        """.format(user_id)
        return self.__execute_cloud_query(query)

    def update_book_quantity(self, book_id, book_quantity):
        """
        Validate the data and prevent SQL Injection attack with
        parametrised query then update data into database
        """
        query = """
            UPDATE Book
            SET Quantity = '{}'
            WHERE BookID = '{}'
        """.format(book_quantity, book_id)
        if self.__validate_record(book_id, book_quantity):
            self.__execute_cloud_query(query)

    def update_record(self, record_id, status, returned_date):
        """
        Validate the data and prevent SQL Injection attack with
        parametrised query then update data into database
        """
        query = """
            UPDATE Record
            SET Status = '{}',
            ReturnedDate = '{}'
            WHERE RecordID = '{}'
        """.format(status, returned_date, record_id)
        if self.__validate_record(record_id, status):
            self.__execute_cloud_query(query)

    def __del__(self):
        self.__connection.close()


class Network():
    """
    Network class to communicate between device (RP and MP)
    """

    def __init__(self, address=ADDRESS, buffer=BUFFER):
        self.__socket = None
        self.__connection = None
        self.__reception_address = None
        self.__username = None
        self.__address = address
        self.__buffer = buffer

    def configure(self, soc):
        """
        Configure socket, connection and address
        This method will wait until Reception PI is connected
        """
        # Set socket
        self.__socket = soc
        # Bind server to selected address
        self.__socket.bind(self.__address)
        # Wait for incoming connection
        self.__socket.listen()
        print("Listening on {}...".format(self.__address))
        # Incoming connection
        self.__connection, self.__reception_address = self.__socket.accept()
        # Wait for username
        self.__username = self.__connection.recv(self.__buffer).decode()
        # Send confirmation to establish connection + welcome message
        self.__connection.sendall("Success!".encode())

    def get_connection(self):
        """
        Getter for connection
        """
        return self.__connection

    def get_reception_address(self):
        """
        Getter for Reception PI address
        """
        return self.__reception_address

    def get_username(self):
        """
        Getter for username
        """
        return self.__username

    def send_message(self, message):
        """
        Send Message
        """
        self.__connection.sendall(message.encode())

    def recv_message(self):
        """
        Listen for message and return message
        """
        message = self.__connection.recv(self.__buffer)
        return message.decode()

    def disconnect(self):
        """
        Disconnect when Reception PI closed connection
        """
        print(self.__username,
              "from",
              self.__reception_address,
              "is disconnected")


class Master():
    """
    Master PI
    """

    def __init__(self, database=Database()):
        self.__database = database

    @classmethod
    def menu(cls):
        """
        Menu interface
        """
        menu = """
            Menu
            1. Search Book Catalogue
            2. Borrow
            3. Return
            4. List All Books
            5. List Borrowed Books
            6. Disconnect
        """
        return menu

    @classmethod
    def __exit(cls, message):
        """
        Check for exit input in console
        """
        exit_command = [
            "6",
            "exit",
            "quit",
            "disconnect"
        ]
        if message in exit_command:
            return True
        return False

    @classmethod
    def __wait_for_user(cls, network):
        """
        Wait until user input an option
        """
        while True:
            data = network.recv_message()
            if data.encode():
                return data

    def __search_book(self, network):
        """
        Search Book
        """
        # Told Reception Pi it a sub menu
        network.send_message("submenu")
        # Send Searh Option
        network.send_message("""
            Search By
            1. Title
            2. Author
            3. ISBN
        """)
        # Wait for Reception Pi response
        search_option = self.__wait_for_user(network)
        # Run search on each option
        if search_option == "1":
            # Told Reception Pi it a sub menu
            network.send_message("submenu")
            # Ask for input
            network.send_message("Title : (Book Title)")
            # Wait for Reception Pi response
            title = self.__wait_for_user(network)
            return self.__database.read_book(title=title)
        if search_option == "2":
            # Told Reception Pi it a sub menu
            network.send_message("submenu")
            # Ask for input
            network.send_message("Author : (Author Name)")
            # Wait for Reception Pi response
            author = self.__wait_for_user(network)
            return self.__database.read_book(author=author)
        if search_option == "3":
            # Told Reception Pi it a sub menu
            network.send_message("submenu")
            # Ask for input
            network.send_message("ISBN : (ISBN Number)")
            # Wait for Reception Pi response
            isbn = self.__wait_for_user(network)
            return self.__database.read_book(isbn=isbn)
        return "Error! Please input a valid option"

    def __borrow_book(self, user_id, books):
        """
        Update Record for borrowed book
        """
        for book_id, _, _, _, quantity in books:
            if quantity <= 0:
                return False
            # Update Record
            self.__database.insert_record(
                user_id,
                book_id,
                'borrowed',
                1,
                datetime.datetime.now()
            )
            # Update Book Quantity
            self.__database.update_book_quantity(book_id, quantity - 1)
        return True

    def __borrow_books(self, network, user_id):
        """
        Borrow Multiple Books
        """
        # Told Reception Pi it a sub menu
        network.send_message("submenu")
        # Send Borrow Book Option
        network.send_message("""
            Borrow By
            1. Title
            2. ISBN
            To borrow multiple book: book1|book2|book3
        """)
        # Wait for Reception Pi response
        borrow_option = self.__wait_for_user(network)
        # Run borrow on each option
        if borrow_option == "1":
            # Told Reception Pi it a sub menu
            network.send_message("submenu")
            # Ask for input
            network.send_message("Title : (Book Title1|Book Title2)")
            # Wait for Reception Pi response
            responses = self.__wait_for_user(network)
        elif borrow_option == "2":
            # Told Reception Pi it a sub menu
            network.send_message("submenu")
            # Ask for input
            network.send_message("ISBN : (Book ISBN1|Book ISBN2)")
            # Wait for Reception Pi response
            responses = self.__wait_for_user(network)
        else:
            return "Error! Please input a valid option"

        # Borrow Book
        for response in responses.split("|"):
            if borrow_option == "1":
                books = self.__database.read_book(title=response)
            else:
                books = self.__database.read_book(isbn=response)
            if not books:
                # No Book
                return "Failed!"
            if not self.__borrow_book(user_id, books):
                # Quantity is 0
                return "Failed!"
        return "Success!"

    def __return_book(self, book_id, record_id):
        """
        Update Record for borrowed book
        """
        # Update Record
        self.__database.update_record(
            record_id,
            'returned',
            datetime.datetime.now()
        )
        # Get Book Quantity
        for _, _, quantity in self.__database.read_book_from_id(book_id):
            # Update Book Quantity
            self.__database.update_book_quantity(book_id, quantity + 1)
        return True

    def __return_books(self, network, user_id):
        """
        Return Multiple Books
        """
        # Told Reception Pi it a sub menu
        network.send_message("submenu")
        # Send Return Book Option
        network.send_message("""
            Return By
            1. Title
            2. ISBN
            To return multiple book: book1|book2|book3
        """)
        # Wait for Reception Pi response
        return_option = self.__wait_for_user(network)
        # Run return on each option
        if return_option == "1":
            # Told Reception Pi it a sub menu
            network.send_message("submenu")
            # Ask for input
            network.send_message("Title : (Book Title1|Book Title2)")
            # Wait for Reception Pi response
            responses = self.__wait_for_user(network)
        elif return_option == "2":
            # Told Reception Pi it a sub menu
            network.send_message("submenu")
            # Ask for input
            network.send_message("ISBN : (Book ISBN1|Book ISBN2)")
            # Wait for Reception Pi response
            responses = self.__wait_for_user(network)
        else:
            return "Error! Please input a valid option"

        # Get user borrowed record
        records = self.__database.read_borrowed_record(user_id)
        # Store all BookID and RecordID
        book_ids = []
        record_ids = []
        for record_id, book_id, _ in records:
            book_ids.append(book_id)
            record_ids.append(record_id)
        # Return Book
        for response in responses.split("|"):
            # Check if book_id match the borrowed book
            if return_option == "1":
                book_id = self.__database.get_book_id(title=response)[0][0]
            else:
                book_id = self.__database.get_book_id(isbn=response)[0][0]
            record_id = record_ids[book_ids.index(book_id)]
            if book_id not in book_ids:
                # No Book
                return "Failed!"
            if not self.__return_book(book_id, record_id):
                # Failed
                return "Failed!"
            book_ids.remove(book_id)
            record_ids.remove(record_id)
        return "Success!"

    def __list_all_books(self):
        """
        List all books
        """
        return self.__database.read_all_book()

    def __list_borrowed_books(self, user_id):
        """
        List book borrowed by user
        """
        response = str()
        records = self.__database.read_borrowed_record(user_id)
        for _, book_id, borrowed_date in records:
            book = self.__database.read_book_from_id(book_id)
            for title, isbn, _ in book:
                response += (
                    title + "\t"
                    + isbn + "\t"
                    + str(borrowed_date) + "\n"
                )
        return response

    @classmethod
    def __beautify_query_result(cls, query_result):
        """
        Re-format tuple into string with tab and newline
        """
        result = ""
        # attributes[0] is ID
        for attributes in query_result:
            if len(attributes) > 1:
                result += str(attributes[1])
            for attribute in attributes[2:]:
                result += "\t" + str(attribute)
            result += "\n"
        return result

    def manage(self, option, network):
        """
        Manage the application
        """
        # Get UserID
        user_id = self.__database.get_user_id(network.get_username())[0][0]
        # Convert to lower case
        option = option.lower()
        # Store database output
        result = ""
        valid_input = False
        if option == "1" or option.startswith("title"):
            # Search
            result = self.__search_book(network)
            # Re-format query result
            result = self.__beautify_query_result(result)
            valid_input = True
        elif option == "2" or option.startswith("borrow"):
            # Borrow
            result = self.__borrow_books(network, user_id)
            valid_input = True
        elif option == "3" or option.startswith("return"):
            # Return
            result = self.__return_books(network, user_id)
            valid_input = True
        elif option == "4" or option.startswith("list a"):
            # List all book
            result = self.__list_all_books()
            # Re-format query result
            result = self.__beautify_query_result(result)
            valid_input = True
        elif option == "5" or option.startswith("list b"):
            # List all book
            result = self.__list_borrowed_books(user_id)
            valid_input = True
        elif option.startswith("help"):
            # Help
            return self.menu()
        elif self.__exit(option):
            return "Disconnect!"
        # Check if user input is valid
        if valid_input:
            # If result exist
            if result:
                return result
            return "No Result!"
        return "Please input a valid option"

    def run_user_check(self, username):
        """
        If new user logged in register in the cloud database
        """
        if not self.__database.read_user(username):
            self.__database.insert_user(username)
            print("User %s is registered" % username)

    def __del__(self):
        del self.__database


def main():
    """
    Main Method
    """
    # Initialization
    network = Network()
    master = Master()
    # Wait for Reception PI
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
        # Configure the network and wait for Reception PI
        network.configure(soc)
        # Check for new user
        master.run_user_check(network.get_username())
        # Reception PI Connected
        with network.get_connection():
            # Send welcome message and menu
            network.send_message(
                "Welcome {}\n{}".format(
                    network.get_username(),
                    master.menu()
                )
            )
            # Print out connected user detail
            print(network.get_username(),
                  "is connected from",
                  network.get_reception_address())
            # Start communication
            while True:
                # Wait for message
                data = network.recv_message()
                if data.encode():
                    # Message Received
                    print("Received {} bytes of data decoded to: '{}'".format(
                        len(data.encode()), data))
                    # Manage the command
                    message = master.manage(data, network)
                    # Reply the result
                    print("Sending data back.")
                    network.send_message(message)
                    # Reception PI disconnected
                    if message == "Disconnect!":
                        network.disconnect()
                        break
            # Disconnected
            print("Disconnecting from client.")
        # Close connection
        print("Closing listening socket.")
    # Close socket
    print("Done.")
    # Close database connection
    del network
    del master


if __name__ == "__main__":
    main()
