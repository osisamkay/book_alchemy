import os
import secrets

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Create a Flask application
app = Flask(__name__)
current_directory = os.path.dirname(os.path.abspath(__file__))
database_path = os.path.join(current_directory, 'data', 'book.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create a SQLAlchemy instance and link it to the Flask app
db = SQLAlchemy(app)

# Generate a random secret key
app.secret_key = secrets.token_hex(16)


# Define the Author model
class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    birth_date = db.Column(db.String, nullable=True)
    date_of_death = db.Column(db.String, nullable=True)

    def __repr__(self):
        return f"<Author id={self.id}, name={self.name}>"


# Define the Book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.String(13), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    author = db.relationship('Author', backref=db.backref('books', lazy=True))

    def __repr__(self):
        return f"<Book id={self.id}, title={self.title}>"

# Uncomment the following line to create the tables
# with app.app_context():
#     db.create_all()
