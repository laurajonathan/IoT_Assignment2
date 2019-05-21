import sys
sys.path.append("..")
import unittest
import socket
import master_main
HOST = "127.0.0.1"  # Empty string means to listen on all IP's on the machine.
PORT = 65000  # Port to listen on (non-privileged ports are > 1023).
ADDRESS = (HOST, PORT)
BUFFER = 4096

class Test_socket(unittest.TestCase):      
    def setUp(self):
        #self.reception = reception_main.Network(ADDRESS, BUFFER)
        self.master = master_main.Network() 
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
            self.master.configure(soc)
            self.master.send_message('test message')
            
    def tearDown(self):
        try:
            self.master.disconnect()
        except:
            pass    

    def test_master_send_message(self):
        self.master.send_message("test message")
        

    #def test(self):
        #server = Network()
        #server.start()
        #client = gevent.socket.create_connection(('127.0.0.1', server.server_port))
        #response = client.makefile().read()
        #assert response == 'hello and goodbye!'
        #server.stop()