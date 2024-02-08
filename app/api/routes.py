from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Book, book_schema, books_schema

api = Blueprint('api',__name__, url_prefix='/api')

# add new books
@api.route('/books', methods = ['POST'])
@token_required
def add_book(current_user_token):
    title = request.json['title']
    author = request.json['author']
    series = request.json['series']
    genre = request.json['genre']
    isbn = request.json['isbn']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    book = Book(title, author, series, genre, isbn, user_token = user_token)

    db.session.add(book)
    db.session.commit()

    response = book_schema.dump(book)
    return jsonify(response)

# get all books
@api.route('/books', methods = ['GET'])
@token_required
def get_book(current_user_token):
    user = current_user_token.token
    books = Book.query.filter_by(user_token = user).all()
    response = books_schema.dump(books)
    return jsonify(response)

# get a specific book
@api.route('/books/<id>', methods = ['GET'])
@token_required
def get_book_by_id(current_user_token, id):
    book = Book.query.get(id)
    response = book_schema.dump(book)
    return jsonify(response)

# update an already existing book
@api.route('/books/<id>', methods = ['POST', 'PUT'])
@token_required
def update_book(current_user_token, id):
    book = Book.query.get(id)
    book.title = request.json['title']
    book.author = request.json['author']
    book.series = request.json['series']
    book.genre = request.json['genre']
    book.isbn = request.json['isbn']
    book.user_token = current_user_token.token

    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)
    
# delete a book
@api.route('/books/<id>', methods = ['DELETE'])
@token_required
def delete_book(current_user_token, id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)