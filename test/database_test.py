import unittest
import reception_main
import MySQLdb
from reception_main import Database as ReceptionDatabase
#from master_main import Database


class test_data(unittest.TestCase):
    HOST = "localhost"
    USER = "pi"
    PASSWORD = "suwat513"
    DATABASE = "TestUser"

    def setup(self):
        self.connection = MySQLdb.connect(test_data.HOST, test_data.USER,
            test_data.PASSWORD, test_data.DATABASE)
        
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
            cursor.execute("insert into Users (username, password, firstname, lastname, email, type)values ('test1', 'abc123', 'bill', 'bob', '1@1.com', 'user')")
            cursor.execute("insert into Users (username, password, firstname, lastname, email, type)values ('test2', 'abc123', 'max', 'man', '2@2.com', 'user')")
            cursor.execute("insert into Users (username, password, firstname, lastname, email, type)values ('test3', 'abc123', 'sam', 'cat', '3@3.com', 'user')")
        self.connection.commit()
        
    def tearDown(self):
        try:
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
        db = ReceptionDatabase(self.connection)
        count = self.countUsers()
        db.insert_data('test4', 'abc123', 'max', 'time', '4@4.com', 'user')
        self.assertTrue(count + 1 == self.countUsers())
        db.insert_data('test5', 'abc123', 'tom', 'mark', '5@5.com', 'user')
        self.assertTrue(count + 2 == self.countUsers())
        del db

    def test_validate_data(self):
        db = ReceptionDatabase(self.connection)
        self.assertTrue(db.__validate_data('test4', 'abc123', 'max', 'time', '4@4.com', 'user'))
        self.assertFalse(db.__validate_data('test4', 'abc123', 'max', 'time', 5, 'user'))
        del db
    
    def test_execute_query(self):
        db = ReceptionDatabase(self.connection)
        query = """select count(*) from User"""
        count = self.countUsers()
        query_count = db.__execute_query(query)
        self.assertEquals(query_count, count)
        del db

    def test_read_data(self):
        db = ReceptionDatabase(self.connection)
        user = "test1"
        expected = ("test1 abc123")
        user_details = db.read_data(user)
        self.assertEquals(user_details, expected)
        del db


if __name__ == "__main__":
    unittest.main()
    



        