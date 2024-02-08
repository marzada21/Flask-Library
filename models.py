from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid 
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager
from flask_marshmallow import Marshmallow 
import secrets

login_manager = LoginManager()
ma = Marshmallow()
db = SQLAlchemy()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(150), nullable=True, default='')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True, default = '')
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default = '', unique = True )
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __init__(self, email, first_name='', last_name='', password='', token='', g_auth_verify=False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self, length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f'User {self.email} has been added to the database'
    
class Book(db.Model):
    id = db.Column(db.String, primary_key = True)
    title = db.Column(db.String(150), nullable = False)
    author = db.Column(db.String(200))
    series = db.Column(db.String(200))
    genre = db.Column(db.String(200))
    isbn = db.Column(db.String(250))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, title, author, series, genre, isbn, user_token, id = ''):
        self.id = self.set_id()
        self.title = title
        self.author = author
        self.series = series
        self.genre = genre
        self.isbn = isbn
        self.user_token = user_token

    def __repr__(self):
        return f'{self.title} by {self.author} has been added to the Library'
    
    def set_id(self):
        return (secrets.token_urlsafe())
    
class BookSchema(ma.Schema):
    class Meta:
        fields = ['id', 'title', 'author', 'series', 'genre', 'isbn']

book_schema = BookSchema()
books_schema = BookSchema(many = True)