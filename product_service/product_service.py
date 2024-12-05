from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Use SQLite database instead of PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///product_db.db'  # Local SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking to save resources

db = SQLAlchemy(app)

# Define the Product model with necessary fields
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)

# Create Product
@app.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()

    # Check if all required fields are provided
    if not all(key in data for key in ['name', 'description', 'price', 'stock']):
        return jsonify({"message": "Missing required fields"}), 400

    new_product = Product(
        name=data['name'],
        description=data['description'],
        price=data['price'],
        stock=data['stock']
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "Product created successfully!"}), 201


# Get Product by ID
@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = db.session.get(Product, product_id)  # Use session.get() instead of query.get()
    if product:
        return jsonify({
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "stock": product.stock
        }), 200
    return jsonify({"message": "Product not found"}), 404


# Load predefined products into the database
@app.route('/products/all', methods=['GET'])
def load_predefined_products():
    predefined_products = [
        {
            "name": "Product 1",
            "description": "Description for product 1",
            "price": 100.0,
            "stock": 50
        },
        {
            "name": "Product 2",
            "description": "Description for product 2",
            "price": 150.0,
            "stock": 30
        },
        {
            "name": "Product 3",
            "description": "Description for product 3",
            "price": 200.0,
            "stock": 20
        }
    ]
    
    # Insert the predefined products into the database
    for product_data in predefined_products:
        new_product = Product(
            name=product_data["name"],
            description=product_data["description"],
            price=product_data["price"],
            stock=product_data["stock"]
        )
        db.session.add(new_product)

    db.session.commit()
    return jsonify({"message": "Predefined products loaded successfully!"}), 200

# Main block to run the app
if __name__ == '__main__':
    # Ensure the database is created within the app context
    with app.app_context():
        print("Attempting to create the database and tables...")
        db.create_all()  # Create all tables
        print("Database and tables created successfully.")
    
    # Start the Flask application
    app.run(host='0.0.0.0', port=5002)
