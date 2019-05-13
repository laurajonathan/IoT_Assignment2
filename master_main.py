"""
reception_main.py

Created by  Suwat Tangtragoonviwatt (s3710374)
            Laura Jonathan (s3696013)
            Warren Shipp (s3690682)
            Aidan Afonso (s3660805)

This script is intended to .....

"""

import socket


HOST = ""  # Empty string means to listen on all IP's on the machine.
PORT = 65000  # Port to listen on (non-privileged ports are > 1023).
ADDRESS = (HOST, PORT)
BUFFER = 4096


class Network():
    """
    Network class to communicate between device (RP and MP)
    """

    def __init__(self, address=ADDRESS, buffer=BUFFER):
        self.socket = None
        self.connection = None
        self.reception_address = None
        self.username = None
        self.address = address
        self.buffer = buffer

    def configure(self, soc):
        """
        Configure socket, connection and address
        This method will wait until Reception PI is connected
        """
        # Set socket
        self.socket = soc
        # Bind server to selected address
        self.socket.bind(self.address)
        # Wait for incoming connection
        self.socket.listen()
        print("Listening on {}...".format(self.address))
        # Incoming connection
        self.connection, self.reception_address = self.socket.accept()
        # Wait for username
        self.username = self.connection.recv(self.buffer).decode()
        # Send confirmation to establish connection + welcome message
        self.connection.sendall("Success!".encode())
        # Send welcome message
        self.connection.sendall("Welcome {}".format(self.username).encode())
        # Print out connected user detail
        print(self.username, "is connected from", self.reception_address)

    def get_connection(self):
        """
        Getter for connection
        """
        return self.connection

    def get_reception_address(self):
        """
        Getter for Reception PI address
        """
        return self.reception_address

    def send_message(self, message):
        """
        Send Message
        """
        self.connection.sendall(message)

    def recv_message(self):
        """
        Listen for message and return message
        """
        message = self.connection.recv(self.buffer)
        return message

    def disconnect(self):
        """
        Disconnect when Reception PI closed connection
        """
        print(self.username, "from", self.reception_address, "is disconnected")
        return


class Master():
    """
    Master PI
    """

    def __init__(self):
        pass

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
            4. Logout
        """
        return menu

    def manage(self, option):
        """
        Manage the application
        """

    def run(self):
        """
        Run something
        """


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
        # Reception PI Connected
        with network.get_connection():
            network.send_message(master.menu().encode())
            # Start communication
            while True:
                # Wait for message
                data = network.recv_message()
                if data:
                    # Reception PI disconnected
                    if data.decode() == "Disconnect!":
                        network.disconnect()
                        break
                    # Message Received
                    print("Received {} bytes of data decoded to: '{}'".format(
                        len(data), data.decode()))
                    # Manage the command
                    master.manage(data)
                    # Reply the result
                    print("Sending data back.")
                    network.send_message("test".encode())
            # Disconnected
            print("Disconnecting from client.")
        # Close connection
        print("Closing listening socket.")
    # Close socket
    print("Done.")


if __name__ == "__main__":
    main()
