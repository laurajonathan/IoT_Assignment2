# -*- coding: utf-8 -*-
"""
Created on Sun May  5 14:34:07 2019

@author: suwat
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
        self.address = address
        self.buffer = buffer

    def run(self):
        """
        Run
        """
        # Wait for Reception PI
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
            # Bind server to selected address
            soc.bind(self.address)
            # Wait for incoming connection
            soc.listen()
            print("Listening on {}...".format(self.address))
            # Incoming connection
            conn, addr = soc.accept()
            # Wait for username
            username = soc.recv(self.buffer)
            # Send confirmation to establish connection
            soc.sendall("Success!".encode())
            # Send welcome message
            soc.sendall("Welcome {}".format(username).encode())
            with conn:
                print("Connected to {}".format(addr))
                # Start communication
                while True:
                    data = conn.recv(self.buffer)

                    print("Received {} bytes of data decoded to: '{}'".format(
                        len(data), data.decode()))
                    print("Sending data back.")
                    conn.sendall(data)

                print("Disconnecting from client.")
            print("Closing listening socket.")
        print("Done.")


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
        option = input("Input (1)Register, (2)Login, (enter)Exit: ")
        while option != "1" and option != "2" and option != "":
            print("Please input (1), (2), or (enter)")
            option = input("Input (1)Register, (2)Login, (enter)Exit: ")
        if option == "1":
            return "Register"
        if option == "2":
            return "Login"
        return ""


def main():
    network = Network()
    network.run()


if __name__ == "__main__":
    main()
