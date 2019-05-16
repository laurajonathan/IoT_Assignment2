from flask import Blueprint, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

api = Blueprint("api", __name__)

db = SQLAlchemy()
ma = Marshmallow()

# Declaring the model.
class Book(db.Model):
    __tablename__ = "Book"
    BookID = db.Column(db.Integer, primary_key = True, autoincrement = True)
    Title = db.Column(db.Text)
    Author = db.Column(db.Text)
    ISBN = db.Column(db.Text)
    Quantity = db.Column(db.Integer)

    def __init__(self, Title, Author, ISBN, Quantity, BookID=None):
        self.BookID = BookID
        self.Title = Title
        self.Author = Author
        self.ISBN = ISBN
        self.Quantity = Quantity

class BookSchema(ma.Schema):
    # Reference: https://github.com/marshmallow-code/marshmallow/issues/377#issuecomment-261628415
    def __init__(self, strict = True, **kwargs):
        super().__init__(strict = strict, **kwargs)
    
    class Meta:
        # Fields to expose.
        fields = ("BookID", "Title", "Author", "ISBN", "Quantity")

bookSchema = BookSchema()
booksSchema = BookSchema(many = True)

# Endpoint to show all book.
@api.route("/book", methods = ["GET"])
def getBook():
    book = Book.query.all()
    result = booksSchema.dump(book)

    return jsonify(result.data)

# Endpoint to get book by id.
@api.route("/book/<id>", methods = ["GET"])
def getBookByID(id):
    book = Book.query.get(id)

    return bookSchema.jsonify(book)

# Endpoint to add new book.
@api.route("/book", methods = ["POST"])
def addBook():
    title = request.form.get('title')
    author = request.form.get('author')
    isbn = request.form.get('isbn')
    quantity = request.form.get('quantity')

    newBook = Book(title, author, isbn, quantity)

    db.session.add(newBook)
    db.session.commit()

    return redirect(url_for('site.index'))
    #return bookSchema.jsonify(newBook)

# Endpoint to delete book.
@api.route("/book/<id>", methods = ["DELETE"])
def bookDelete(id):
    book = Book.query.get(id)

    db.session.delete(book)
    db.session.commit()

    return bookSchema.jsonify(book)
