import os
import sqlite3
import datetime
from functools import wraps
from flask import Flask, request, jsonify, send_from_directory
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
import json

app = Flask(__name__, static_folder='.')
app.config['SECRET_KEY'] = 'co2-cafe-secret-key-123'  # In production, use a secure key
DATABASE = 'database.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS carts (
            user_id INTEGER PRIMARY KEY,
            cart_data TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    conn.commit()
    conn.close()

# Initialize DB on startup
init_db()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            conn = get_db()
            user = conn.execute('SELECT * FROM users WHERE id = ?', (data['user_id'],)).fetchone()
            conn.close()
            if not user:
                raise Exception("User not found")
        except Exception as e:
            return jsonify({'message': 'Token is invalid!', 'error': str(e)}), 401
            
        return f(user, *args, **kwargs)
    return decorated

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'message': 'Missing email or password'}), 400
        
    hashed_password = generate_password_hash(password)
    
    conn = get_db()
    try:
        conn.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, hashed_password))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'message': 'User already exists'}), 409
    
    conn.close()
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    conn.close()
    
    if not user or not check_password_hash(user['password'], password):
        return jsonify({'message': 'Invalid credentials'}), 401
        
    token = jwt.encode({
        'user_id': user['id'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
    }, app.config['SECRET_KEY'], algorithm='HS256')
    
    return jsonify({'token': token}), 200

@app.route('/api/cart', methods=['GET'])
@token_required
def get_cart(current_user):
    conn = get_db()
    cart = conn.execute('SELECT cart_data FROM carts WHERE user_id = ?', (current_user['id'],)).fetchone()
    conn.close()
    
    if cart:
        return jsonify({'cart': json.loads(cart['cart_data'])}), 200
    return jsonify({'cart': {}}), 200

@app.route('/api/cart', methods=['POST'])
@token_required
def save_cart(current_user):
    data = request.get_json()
    cart_data = data.get('cart', {})
    
    conn = get_db()
    conn.execute('''
        INSERT INTO carts (user_id, cart_data) VALUES (?, ?)
        ON CONFLICT(user_id) DO UPDATE SET cart_data = excluded.cart_data
    ''', (current_user['id'], json.dumps(cart_data)))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Cart saved successfully'}), 200

@app.route('/api/checkout', methods=['POST'])
@token_required
def checkout(current_user):
    # In a real app, integrate payment gateway here.
    # For now, just clear the cart.
    conn = get_db()
    conn.execute('DELETE FROM carts WHERE user_id = ?', (current_user['id'],))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Checkout successful! Your order is being processed.'}), 200

# Serve static files from the root directory
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    if os.path.exists(path):
        return send_from_directory('.', path)
    return "Not Found", 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
