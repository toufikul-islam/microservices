import unittest
from user_service import app, db
from user_service import User

class UserServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        # Reset the database before each test
        with app.app_context():
            db.drop_all()  # Drop all tables
            db.create_all()  # Create new tables (empty)

    def test_create_user(self):
        response = self.app.post('/users', json={'name': 'John Doe', 'email': 'john@example.com', 'password': 'password123'})
        self.assertEqual(response.status_code, 201)

    def test_get_user(self):
        self.app.post('/users', json={'name': 'John Doe', 'email': 'john@example.com', 'password': 'password123'})
        response = self.app.get('/users/1')
        self.assertEqual(response.status_code, 200)

    def test_create_user_missing_fields(self):
        response = self.app.post('/users', json={'name': 'John Doe'})
        self.assertEqual(response.status_code, 400)  # Should return 400 due to missing fields

    def test_get_all_users(self):
        # Ensure the predefined users are added only once
        response = self.app.get('/users/all')
        self.assertEqual(len(response.json['users']), 3)  # Expecting 3 predefined users
        
    def test_get_non_existent_user(self):
        response = self.app.get('/users/9999')  # Non-existent user ID
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
