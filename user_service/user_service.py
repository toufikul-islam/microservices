from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app = Flask(__name__)

# Predefined database URI (for a local SQLite database)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking

# Initialize the SQLAlchemy object
db = SQLAlchemy(app)

# Define the User model for SQLAlchemy
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Predefined route to create a new user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()  # Get data from the request body
    
    # Check if required fields are present
    if not data.get('name') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing required fields (name, email, password)'}), 400

    new_user = User(
        name=data.get('name'),
        email=data.get('email'),
        password=data.get('password')
    )
    db.session.add(new_user)
    db.session.commit()  # Commit changes to the database
    return jsonify({"message": "User created successfully!"}), 201

# Predefined route to get a user by ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = db.session.get(User, user_id)  # Using session.get() instead of legacy query.get()
    if user:
        return jsonify({"id": user.id, "name": user.name, "email": user.email}), 200
    return jsonify({"message": "User not found"}), 404

# Predefined route to get all users
@app.route('/users/all', methods=['GET'])
def add_users_and_return_all():
    # Predefined data to add to the database
    predefined_users = [
        {"name": "Alice", "email": "alice@example.com", "password": "password123"},
        {"name": "Bob", "email": "bob@example.com", "password": "password456"},
        {"name": "Charlie", "email": "charlie@example.com", "password": "password789"}
    ]
    
    # Add the predefined users to the database only if they do not exist
    for user_data in predefined_users:
        existing_user = User.query.filter_by(email=user_data['email']).first()
        # if not existing_user:
        if existing_user:
            print(f"User with email {user_data['email']} already exists.")
        else:
            new_user = User(
                name=user_data['name'],
                email=user_data['email'],
                password=user_data['password']
            )
            db.session.add(new_user)
    
    db.session.commit()  # Commit changes to the database
    
    # Fetch all users after insertion
    users = User.query.all()
    users_data = [{"id": user.id, "name": user.name, "email": user.email} for user in users]
    
    return jsonify({"message": "Predefined users added to the database!", "users": users_data}), 200

# Application entry point
if __name__ == '__main__':
    # Ensure the database and tables are created within the app context
    with app.app_context():
        print("Attempting to create the database and tables...")
        db.create_all()  # Create all tables if they don't already exist
        print("Database and tables created successfully.")
    
    # Start the Flask application
    app.run(host='0.0.0.0', port=5001)
