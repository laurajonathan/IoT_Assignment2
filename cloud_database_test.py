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
    DATABASE = "Test"

    def setUp(self):
        print("Testing: ", self._testMethodName)
        self.connection = MySQLdb.connect(test_data_cloud.HOST, test_data_cloud.USER, test_data_cloud.PASSWORD, test_data_cloud.DATABASE)
        self.db = MasterDatabase(self.connection)
        with self.connection.cursor() as cursor:
            cursor.execute("drop table if exists Book")
            cursor.execute("""
                create table if not exists Book(
                    BookID int not null auto_increment,
                    Title text not null,
                    Author text not null,
                    ISBN text not null,
                    Quantity int not null,
                    constraint PK_Book primary key (BookID) 
                )""")
            cursor.execute("insert into Book (Title, Author, ISBN, Quantity)values ('book1', 'author1', '1', 5)")
            cursor.execute("insert into Book (Title, Author, ISBN, Quantity)values ('book2', 'author2', '2', 5)")
            cursor.execute("drop table if exists Record")
            cursor.execute("""
                create table if not exists Record(
                    RecordID int not null auto_increment,
                    UserID int not null,
                    BookID int not null,
                    Status text not null,
                    Quantity int not null,
                    BorrowedDate datetime not null,
                    ReturnedDate datetime null,
                    constraint PK_Record primary key (RecordID)
                )""")
        self.connection.commit()
        
    def tearDown(self):
        try:
            self.db.connection.close()
            self.connection.close()
        except:
            pass
        finally:
            self.connection = None

    def countBooks(self):
        """
        Function to get number of books in table
        """
        with self.connection.cursor() as cursor:
            cursor.execute("select count(*) from Book")
            return cursor.fetchone()[0]

    def countRecords(self):
        """
        Function to get number of records in table
        """
        with self.connection.cursor() as cursor:
            cursor.execute("select count(*) from Record")
            return cursor.fetchone()[0]

    def getBookQuantity(self, id):
        """
        Function to get number of books with a given ID
        """
        with self.connection.cursor() as cursor:
            cursor.execute("select Quantity from Book where BookID = '{}'".format(id))
            return cursor.fetchone()[0]
        
    def checkRecord(self, id):
        """
        Function to get the number of records with given id
        """
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT Status FROM Record WHERE RecordID = '{}'".format(id))
            return cursor.fetchone()[0]

    def test_insert_record(self):
        """
        Test to insert records into the table
        """
        date = datetime.datetime.now()
        count = self.countRecords()
        self.db.insert_record(1, 1,'borrowed', 1, date)
        self.db.insert_record(1, 1,'borrowed', 1, date)
        self.assertEqual(count + 2, self.countRecords())
		
    def test_read_book_funcs(self):
        """
        Test to read the book details
        """
        booktitle = "book1"
        bookauthor = "author1"
        bookisbn = '1'
        bookdetails = self.db.read_book(booktitle, bookauthor, bookisbn)
        self.assertEqual(bookdetails, ((1, 'book1', 'author1', '1', 5),))

    def test_read_book_funcs_id(self):
        """
        Test to read the book details with a given id
        """
        bookdetails = self.db.read_book_from_id('1')
        self.assertEqual(bookdetails, (('book1', '1', 5),))

    def test_read_all_book(self):
        """
        Test to list all the books in the given table
        """
        allbooks = self.db.read_all_book()
        expected = ((1, 'book1', 'author1', '1', 5), (2, 'book2', 'author2', '2', 5))
        self.assertEqual(allbooks, expected)
		
    def test_read_borrowed(self):
        """
        Test to list all the books that have the borrowed status
        """
        date = datetime.datetime.now()
        self.db.insert_record(1, 1,'borrowed', 1, date)
        borrowed = self.db.read_borrowed_record('1')
        borrowedid = borrowed[0]
        self.assertEqual(borrowedid[0], 1)
    
    def test_update_book_quantity(self):
        """
        Test to update the quantity of books in the given table
        """
        expected_quantity = 10
        self.db.update_book_quantity(2, 10)
        quantity = self.getBookQuantity(2)
        self.assertEqual(quantity, expected_quantity)

    def test_update_record(self):
        """
        Test to update the record of the book 
        """
        date = datetime.datetime.now()
        self.db.insert_record(1, 1,'borrowed', 1, date)
        self.db.update_record(1, 'returned', date)
        record_status = self.checkRecord(1)
        self.assertEqual(record_status, 'returned')
        
if __name__ == "__main__":
    unittest.main()