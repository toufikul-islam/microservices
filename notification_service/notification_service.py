from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notifications.db'  # Use SQLite for simplicity
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Notification model
class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    payment_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    message = db.Column(db.String(200), nullable=False)
    notification_type = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Notification {self.id}>'

# Route to send a notification
@app.route('/notifications', methods=['POST'])
def send_notification():
    data = request.get_json()

    # Validate input data
    if not data or 'user_id' not in data or 'message' not in data or 'notification_type' not in data:
        return jsonify({"message": "Invalid input data"}), 400

    try:
        # Simulate sending notification to external service
        response = requests.post('https://mocknotificationapi.com/send', json=data)

        if response.status_code == 200:
            new_notification = Notification(
                user_id=data['user_id'],
                payment_id=data['payment_id'],
                message=data['message'],
                notification_type=data['notification_type'],
                status='Sent'
            )
            db.session.add(new_notification)
            db.session.commit()
            return jsonify({"message": "Notification sent successfully!"}), 200
        else:
            return jsonify({"message": "Failed to send notification."}), 500

    except requests.RequestException:
        return jsonify({"message": "Error sending notification."}), 500

# Route to get all notifications
@app.route('/notifications/all', methods=['GET'])
def get_notifications():
    notifications = Notification.query.all()  # Retrieve all notifications from the database
    if not notifications:  # Check if no notifications are found
        return jsonify({'message': 'No data found'}), 404
    result = []
    for notification in notifications:
        result.append({
            'id': notification.id,
            'user_id': notification.user_id,
            'payment_id':notification.payment_id,
            'message': notification.message,
            'notification_type': notification.notification_type,
            'status': notification.status
        })
    return jsonify(result), 200

# Route to get notification by ID
@app.route('/notifications/<int:id>', methods=['GET'])
def get_notification_by_id(id):
    notification = Notification.query.get(id)
    if notification:
        return jsonify({
            'id': notification.id,
            'user_id': notification.user_id,
            'payment_id':notification.payment_id,
            'message': notification.message,
            'notification_type': notification.notification_type,
            'status': notification.status
        }), 200
    else:
        return jsonify({"message": "Notification not found"}), 404


# Application entry point
if __name__ == '__main__':
    # Ensure the database and tables are created within the app context
    with app.app_context():
        print("Attempting to create the database and tables...")
        db.create_all()  # Create all tables if they don't already exist
        print("Database and tables created successfully.")
    
    # Start the Flask application
    app.run(host='0.0.0.0', port=5005)
