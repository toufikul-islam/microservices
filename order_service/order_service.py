from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)

# Using SQLite instead of PostgreSQL for the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///order_db.db'  # Local SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking to save resources

db = SQLAlchemy(app)

# Define the Order model with necessary fields
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False, default="Pending")

# Create an Order
@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    
    # Check if the user exists by calling the user service
    user_response = requests.get(f'http://user_service:5001/users/{data["user_id"]}')
    if user_response.status_code != 200:
        return jsonify({"message": "User not found"}), 404

    # Check if the product exists by calling the product service
    product_response = requests.get(f'http://product_service:5002/products/{data["product_id"]}')
    if product_response.status_code != 200:
        return jsonify({"message": "Product not found"}), 404

    product = product_response.json()
    if product["stock"] < data["quantity"]:
        return jsonify({"message": "Insufficient stock"}), 400

    total_price = product["price"] * data["quantity"]
    new_order = Order(
        user_id=data['user_id'],
        product_id=data['product_id'],
        quantity=data['quantity'],
        total_price=total_price
    )
    db.session.add(new_order)
    db.session.commit()
    return jsonify({"message": "Order created successfully!", "order_id": new_order.id}), 201

# Get Order by ID
@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    # order = Order.query.get(order_id)
    order = db.session.get(Order, order_id)
    if order:
        return jsonify({
            "id": order.id,
            "user_id": order.user_id,
            "product_id": order.product_id,
            "quantity": order.quantity,
            "total_price": order.total_price,
            "status": order.status
        }), 200
    return jsonify({"message": "Order not found"}), 404

# Load predefined data into the Order table
@app.route('/orders/all', methods=['GET'])
def load_predefined_orders():
    predefined_orders = [
        {
            "user_id": 1,
            "product_id": 1,
            "quantity": 2,
            "total_price": 300.00,
            "status": "Pending"
        },
        {
            "user_id": 2,
            "product_id": 2,
            "quantity": 1,
            "total_price": 150.00,
            "status": "Completed"
        },
        {
            "user_id": 3,
            "product_id": 3,
            "quantity": 5,
            "total_price": 500.00,
            "status": "Pending"
        }
    ]

    # Insert the predefined orders into the database
    for order_data in predefined_orders:
        new_order = Order(
            user_id=order_data["user_id"],
            product_id=order_data["product_id"],
            quantity=order_data["quantity"],
            total_price=order_data["total_price"],
            status=order_data["status"]
        )
        db.session.add(new_order)
    
    db.session.commit()
    return jsonify({"message": "Predefined orders loaded successfully!"}), 200

# Main block to run the app
if __name__ == '__main__':
    # Ensure the database is created within the app context
    with app.app_context():
        print("Attempting to create the database and tables...")
        db.create_all()  # Create all tables
        print("Database and tables created successfully.")
    
    # Start the Flask application
    app.run(host='0.0.0.0', port=5003)
