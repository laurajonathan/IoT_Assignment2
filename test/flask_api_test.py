import sys
sys.path.append("..")
import unittest
import reception_main
from app import app
import flaskr

class TreeTests(unittest.TestCase):

    HOST = "35.197.173.114"
    USER = "root"
    PASSWORD = "suwat513"
    DATABASE = "Test"

    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
        app.testing = True
        self.app = flaskr.app.test_client()

    def tearDown(self):
        pass

    def test_get_book(self):
        rv = self.app.get('/book')
        self.assertEquals(rv, "")

    #def test_get_book_id(self):
        
    
    #def test_bookDelete(self):
        
if __name__ == "__main__":
    unittest.main()