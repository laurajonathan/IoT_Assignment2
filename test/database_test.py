import sys
sys.path.append("..")
import unittest
import MySQLdb
from reception_main import Database as ReceptionDatabase
#from master_main import Database


class test_data(unittest.TestCase):
    HOST = "localhost"
    USER = "pi"
    PASSWORD = "suwat513"
    DATABASE = "TestUser"

    def setUp(self):
        print("Testing: ", self._testMethodName)
        self.connection = MySQLdb.connect(test_data.HOST, test_data.USER, test_data.PASSWORD, test_data.DATABASE)
        self.db = ReceptionDatabase(self.connection)
        with self.connection.cursor() as cursor:
            cursor.execute("drop table if exists User")
            cursor.execute("""
                create table if not exists User (
                    username text not null,
                    password text not null,
                    firstname text not null,
                    lastname text not null,
                    email text not null,
                    type text not null         
                )""")
            cursor.execute("insert into User (username, password, firstname, lastname, email, type)values ('test1', 'abc123', 'bill', 'bob', '1@1.com', 'user')")
            cursor.execute("insert into User (username, password, firstname, lastname, email, type)values ('test2', 'abc123', 'max', 'man', '2@2.com', 'user')")
            cursor.execute("insert into User (username, password, firstname, lastname, email, type)values ('test3', 'abc123', 'sam', 'cat', '3@3.com', 'user')")
        self.connection.commit()
        
    def tearDown(self):
        try:
            self.db.connection.close()
            self.connection.close()
        except:
            pass
        finally:
            self.connection = None

    def countUsers(self):
        with self.connection.cursor() as cursor:
            cursor.execute("select count(*) from User")
            return cursor.fetchone()[0]

    def test_insert_data(self):
        count = self.countUsers()
        self.db.insert_data('test4', 'abc123', 'max', 'time', '4@4.com', 'user')
        self.db.insert_data('test5', 'abc123', 'tom', 'mark', '5@5.com', 'user')
        self.assertTrue(count + 2 == self.countUsers())
    
    def test_read_data(self):
        user = "test1"
        expected = ("test1", "abc123")
        user_details = self.db.read_data(user)
        self.assertEquals(user_details, expected)

if __name__ == "__main__":
    unittest.main()
    



        