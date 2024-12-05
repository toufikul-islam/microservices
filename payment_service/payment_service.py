from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///payment_service.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Model
class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, nullable=False, unique=True)
    user_id = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False)

# Routes
@app.route('/payments', methods=['POST'])
def process_payment():
    try:
        data = request.get_json()
        payment = Payment(
            order_id=data['order_id'],
            user_id=data['user_id'],
            amount=data['amount'],
            status=data['status']
        )
        db.session.add(payment)
        db.session.commit()
        return jsonify({'message': 'Payment processed successfully!', 'payment_id': payment.id}), 201
    except Exception as e:
        print("Error in /payment:", str(e))  # Debugging error
        return jsonify({'error': str(e)}), 500

@app.route('/payments/order/<int:order_id>', methods=['GET'])
def get_payment_by_order(order_id):
    payment = Payment.query.filter_by(order_id=order_id).first()
    if not payment:
        return jsonify({'error': 'Payment not found'}), 404
    return jsonify({
        'order_id': payment.order_id,
        'user_id': payment.user_id,
        'amount': payment.amount,
        'status': payment.status
    }), 200

@app.route('/payments/all', methods=['GET'])
def get_all_payments():
    payments = Payment.query.all()
    if not payments:
        return jsonify({'message': 'No data found'}), 404
    return jsonify([{
        'order_id': payment.order_id,
        'user_id': payment.user_id,
        'amount': payment.amount,
        'status': payment.status
    } for payment in payments]), 200

@app.route('/payments/order/<int:order_id>', methods=['PUT'])
def update_payment(order_id):
    data = request.get_json()
    payment = Payment.query.filter_by(order_id=order_id).first()
    if not payment:
        return jsonify({'error': 'Payment not found'}), 404
    if 'amount' in data:
        payment.amount = data['amount']
    db.session.commit()
    return jsonify({'message': 'Payment updated successfully!', 'new_amount': payment.amount}), 200

@app.route('/payments/order/<int:order_id>', methods=['DELETE'])
def delete_payment(order_id):
    payment = Payment.query.filter_by(order_id=order_id).first()
    if not payment:
        return jsonify({'error': 'Payment not found'}), 404
    db.session.delete(payment)
    db.session.commit()
    return jsonify({'message': f'Payment for order {order_id} deleted successfully!'}), 200

# Application entry point
if __name__ == '__main__':
    # Ensure the database and tables are created within the app context
    with app.app_context():
        print("Attempting to create the database and tables...")
        db.create_all()  # Create all tables if they don't already exist
        print("Database and tables created successfully.")
    
    # Start the Flask application
    app.run(host='0.0.0.0', port=5004)