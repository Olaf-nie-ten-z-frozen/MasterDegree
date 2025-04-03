from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import uuid
import os
import psycopg2

load_dotenv()  # Load .env file

# Instantiate Flask app
app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': 'http://localhost:5173'}})

# Database login data from .env OR hardcoded fallback
USER = os.getenv("user", "postgres")
PASSWORD = os.getenv("password", "yHCRkHnSfzBRSXZm")
HOST = os.getenv("host", "db.lgtebolnnelplqnfxirp.supabase.co")
PORT = os.getenv("port", 5432)
DBNAME = os.getenv("dbname", "postgres")

# Test DB connection
try:
    print("🔌 Connecting to Supabase...")
    conn = psycopg2.connect(
        dbname=os.getenv("dbname"),
        user=os.getenv("user"),
        password=os.getenv("password"),
        host=os.getenv("host"),
        port=os.getenv("port")
    )
    print("✅ Connected to Supabase!")

    cur = conn.cursor()
    cur.execute("SELECT NOW();")
    print("🕒 DB Time:", cur.fetchone())
    cur.close()
    conn.close()
except Exception as e:
    print("❌ Connection failed:", e)

# DB connection helper
def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("dbname"),
        user=os.getenv("user"),
        password=os.getenv("password"),
        host=os.getenv("host"),
        port=os.getenv("port")
    )


@app.route("/books", methods=["GET"])
def get_books():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM books")
        rows = cur.fetchall()
        books = [
            {
                "id": row[0],
                "title": row[1],
                "author": row[2],
                "read": row[3]
            } for row in rows
        ]
        cur.close()
        conn.close()
        return jsonify(books)
    
    except Exception as e:
        print("❌ Error fetching books:", e)
        return jsonify({"error": "Database error"}), 500

@app.route('/books', methods=['GET', 'POST'])
def all_books():
    response_object = {'status': 'success'}

    try:
        conn = get_connection()
        cur = conn.cursor()

        if request.method == 'POST':
            post_data = request.get_json()
            cur.execute("""
                INSERT INTO books (id, title, author, read)
                VALUES (%s, %s, %s, %s)
            """, (
                str(uuid.uuid4()),
                post_data.get('title'),
                post_data.get('author'),
                post_data.get('read', False)
            ))
            conn.commit()

            response_object['message'] = 'Book added!'
            response_object['book'] = {
                'title': post_data.get('title'),
                'author': post_data.get('author'),
                'read': post_data.get('read', False)
            }

        else:  # GET
            cur.execute("SELECT id, title, author, read FROM books")
            rows = cur.fetchall()
            response_object['books'] = [
                {
                    'id': row[0],
                    'title': row[1],
                    'author': row[2],
                    'read': row[3]
                } for row in rows
            ]

        cur.close()
        conn.close()

    except Exception as e:
        print("❌ Error:", e)
        response_object['status'] = 'error'
        response_object['message'] = str(e)

    return jsonify(response_object)
# Define Book model (Not needed with direct get_connection helper method)
# class Book(db.Model):
#     __tablename__ = 'books'

#     id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
#     title = db.Column(db.String, nullable=False)
#     author = db.Column(db.String, nullable=False)
#     read = db.Column(db.Boolean, default=False)

#     def to_dict(self):
#         return {
#             "id": self.id,
#             "title": self.title,
#             "author": self.author,
#             "read": self.read
#         }

# # Sanity check route
# @app.route('/ping', methods=['GET'])
# def ping_pong():
#     return jsonify('pong!')

# # Get or add books
# @app.route('/books', methods=['GET', 'POST'])
# def all_books():
#     response_object = {'status': 'success'}
#     if request.method == 'POST':
#         post_data = request.get_json()
#         new_book = Book(
#             title=post_data.get('title'),
#             author=post_data.get('author'),
#             read=post_data.get('read', False)
#         )
#         db.session.add(new_book)
#         db.session.commit()
#         response_object['message'] = 'Book added!'
#         response_object['book'] = new_book.to_dict()
#     else:
#         books = Book.query.all()
#         response_object['books'] = [book.to_dict() for book in books]
#     return jsonify(response_object)

# # Update or delete a specific book
# @app.route('/books/<book_id>', methods=['PUT', 'DELETE'])
# def single_book(book_id):
#     book = Book.query.get(book_id)
#     if not book:
#         return jsonify({'error': 'Book not found'}), 404

#     if request.method == 'PUT':
#         data = request.get_json()
#         book.title = data.get('title', book.title)
#         book.author = data.get('author', book.author)
#         book.read = data.get('read', book.read)
#         db.session.commit()
#         return jsonify({'message': 'Book updated!', 'book': book.to_dict()})

#     elif request.method == 'DELETE':
#         db.session.delete(book)
#         db.session.commit()
#         return jsonify({'message': 'Book deleted'})
        

if __name__ == '__main__':
    app.run()
