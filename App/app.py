from flask import Flask, jsonify, request, render_template
from flask_mysqldb import MySQL
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# MySQL configuration
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_DB'] = 'bookstore'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Retrieve all books
@app.route('/books', methods=['GET'])
def get_books():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM books")
    books = cur.fetchall()
    cur.close()
    return jsonify(books)

# Add a new book
@app.route('/books', methods=['POST'])
def add_book():
    data = request.json
    title = data['title']
    author = data['author']
    isbn = data['isbn']
    
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO books (title, author, isbn) VALUES (%s, %s, %s)", (title, author, isbn))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Book added successfully'}), 201

# Update a book (ensure only one definition for this function)
@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    data = request.json
    title = data['title']
    author = data['author']
    isbn = data['isbn']
    
    cur = mysql.connection.cursor()
    cur.execute("UPDATE books SET title = %s, author = %s, isbn = %s WHERE id = %s", (title, author, isbn, id))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Book updated successfully'})

# Delete a book
@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM books WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Book deleted successfully'})

# Search for book info using Open Library API
@app.route('/search', methods=['GET'])
def search_book():
    isbn = request.args.get('isbn')
    response = requests.get(f'https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data')
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({'error': 'Book not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
