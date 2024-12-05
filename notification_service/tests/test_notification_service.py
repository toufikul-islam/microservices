import unittest
from notification_service import app, db, Notification
from unittest.mock import patch

class NotificationServiceTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Setup the test environment."""
        cls.app = app.test_client()
        cls.app.testing = True
        with app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        """Tear down the test environment."""
        with app.app_context():
            db.drop_all()

    def setUp(self):
        """Set up for each individual test."""
        with app.app_context():
            db.session.remove()
            db.drop_all()
            db.create_all()

    def tearDown(self):
        """Clean up after each individual test."""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def create_notification(self, user_id, payment_id, message, notification_type, status="Sent"):
        with app.app_context():
            notification = Notification(
                user_id=user_id,
                payment_id=payment_id,
                message=message,
                notification_type=notification_type,
                status=status
            )
            db.session.add(notification)
            db.session.commit()
            return notification

    def test_send_notification_success(self):
        """Test sending a notification successfully."""
        payload = {
            'user_id': 1,
            'payment_id': 1,
            'message': 'Test notification',
            'notification_type': 'email'
        }

        with patch('requests.post') as mock_post:
            mock_post.return_value.status_code = 200
            response = self.app.post('/notifications', json=payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['message'], 'Notification sent successfully!')

    def test_send_notification_failure(self):
        """Test failure in sending notification and storing it in the database."""
        payload = {
            'user_id': 1,
            'payment_id': 1,
            'message': 'Test notification failure',
            'notification_type': 'sms'
        }

        with patch('requests.post') as mock_post:
            mock_post.return_value.status_code = 500
            response = self.app.post('/notifications', json=payload)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.get_json()['message'], 'Failed to send notification.')

    def test_get_notifications_empty(self):
        """Test retrieving notifications when database is empty."""
        response = self.app.get('/notifications/all')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json()['message'], 'No data found')

    def test_get_notifications(self):
        """Test retrieving all notifications."""
        self.create_notification(1, 1, "Test notification", "email")

        response = self.app.get('/notifications/all')
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.get_json()), 0)

    def test_get_notification_by_id(self):
        """Test retrieving a notification by ID."""
        # First, add a notification to the database
        with app.app_context():
            notification = Notification(
                user_id=1,
                payment_id=1,
                message="Test notification",
                notification_type="email",
                status="Sent"
            )
            db.session.add(notification)
            db.session.commit()

            # Explicitly refresh the instance to keep it bound to the session
            db.session.refresh(notification)
            notification_id = notification.id  # Access ID before session ends

        # Test the GET /notifications/<id> route
        response = self.app.get(f'/notifications/{notification_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['id'], notification_id)


        response = self.app.get(f'/notifications/{notification.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['id'], notification.id)

    def test_get_notification_not_found(self):
        """Test retrieving a notification that doesn't exist."""
        response = self.app.get('/notifications/9999')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json()['message'], 'Notification not found')

    def test_send_notification_invalid_payload(self):
        """Test sending a notification with invalid payload."""
        payload = {
            'user_id': 1,
            'message': 'Missing required fields'
        }

        response = self.app.post('/notifications', json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()['message'], 'Invalid input data')


if __name__ == '__main__':
    unittest.main()
