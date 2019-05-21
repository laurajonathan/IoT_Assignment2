import sys
sys.path.append("..")
import unittest
import MySQLdb
from master_main import Database as MasterDatabase
import datetime
#from master_main import Database


class test_data_cloud(unittest.TestCase):
    HOST = "35.197.173.114"
    USER = "root"
    PASSWORD = "suwat513"
    DATABASE = "Assignment2"
          
    def setup(self):
        self.connection = MySQLdb.connect(test_data_cloud.HOST, test_data_cloud.USER,
            test_data_cloud.PASSWORD, test_data_cloud.DATABASE)
        
        with self.connection.cursor() as cursor:
            cursor.execute("drop table if exists testingbook")
            cursor.execute("""
                create table if not exists testingbook(
                    BookID int not null auto_increment,
                    Title text not null,
                    Author text not null,
                    ISBN text not null,
                    Quantity int not null,
                    constraint PK_Book primary key (BookID) 
                )""")
            cursor.execute("insert into testingbook (Title, Author, ISBN, Quantity)values ('book1', 'author1', '1', '5')")
            cursor.execute("insert into testingbook (Title, Author, ISBN, Quantity)values ('book2', 'author2', '2', '5')")
            cursor.execute("insert into testingbook (Title, Author, ISBN, Quantity)values ('book3', 'author3', '3', '5')")
            cursor.execute("drop table if exists testrecords")
            cursor.execute("""
                create table if not exists testrecords (
                    RecordID int not null auto_increment,
                    UserID int not null,
                    BookID int not null,
                    Status text not null,
                    Quantity int not null,
                    BorrowedDate datetime not null,
                    ReturnedDate datetime null,
                    constraint PK_Record primary key (RecordID),
                    constraint FK_Record_User foreign key (UserID) references User (UserID),
                    constraint FK_Record_Book foreign key (BookID) references Book (BookID)
                )""")
            cursor.execute("""insert into testrecords (UserID, BookID, Status,
                            Quantity, BorrowedDate)values ('1', 'book1', 'borrowed', '1', 
                            BorrowedDate = %s""", (datetime.datetime.now()))
        self.connection.commit()
        
    def tearDown(self):
        try:
            self.connection.close()
        except:
            pass
        finally:
            self.connection = None

    def countBooks(self):
        with self.connection.cursor() as cursor:
            cursor.execute("select count(*) from testingbook")
            return cursor.fetchone()[0]

    def countRecords(self):
        with self.connection.cursor() as cursor:
            cursor.execute("select count(*) from testrecords")
            return cursor.fetchone()[0]

    def test_execute_cloud_query(self):
        db = MasterDatabase(self.connection)
        query = """select count(*) from testingbooks"""
        count = self.countBooks()
        query_count = db.__execute_cloud_query(query)
        self.assertEquals(query_count, count)

    def test_validate_record(self):
        db = MasterDatabase(self.connection)
        self.assertTrue(db.__validate_record('book1', 'author1', 'borrowed', '1', '5'))
        self.assertFalse(db.__validate_record('book2', 'author2','borrowed', '1', 5))

    def test_insert_record(self):
        db = MasterDatabase(self.connection)
        count = self.countRecords()
        db.insert_record('book2', 'author2','borrowed', '1', datetime.datetime.now())
        self.assertTrue(count + 1 == self.countRecords())
        db.insert_record('book3', 'author3','borrowed', '1', datetime.datetime.now())
        self.assertTrue(count + 1 == self.countRecords())

    def test_read_book_funcs(self):
        db = MasterDatabase(self.connection)
        booktitle = "book1"
        bookauthor = "author1"
        bookisbn = '1'
        bookdetails = db.read_book(booktitle, bookauthor, bookisbn)
        self.assertEquals(bookdetails, "book1 author1 1")
        bookdetails = db.read_book_from_id('1')
        self.assertEquals(bookdetails, "book1 1 4")

if __name__ == "__main__":
    unittest.main()