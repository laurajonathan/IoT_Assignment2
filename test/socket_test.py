import unittest
import master_main

HOST = ""  # Empty string means to listen on all IP's on the machine.
PORT = 65000  # Port to listen on (non-privileged ports are > 1023).
ADDRESS = (HOST, PORT)
BUFFER = 4096

class Test_socket(unittest.TestCase):      

    def test(self):
        server = Network()
        server.start()
        client = gevent.socket.create_connection(('127.0.0.1', server.server_port))
        response = client.makefile().read()
        assert response == 'hello and goodbye!'
        server.stop()