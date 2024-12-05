import unittest
from order_service import app, db, Order
from unittest.mock import patch
from flask import jsonify

class OrderServiceTestCase(unittest.TestCase):
    def setUp(self):
        """Set up a test client and initialize the database."""
        self.app = app.test_client()
        self.app.testing = True

        # Create a new database for each test
        with app.app_context():
            db.create_all()

    def tearDown(self):
        """Clean up the database after each test."""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    @patch('order_service.requests.get')
    def test_create_order_success(self, mock_get):
        """Test creating an order successfully."""
        # Mock the user and product service responses
        mock_get.side_effect = [
            unittest.mock.Mock(status_code=200),  # User service response
            unittest.mock.Mock(status_code=200, json=lambda: {'price': 150.00, 'stock': 10})  # Product service response
        ]
        
        # Simulate POST request to create an order
        with app.app_context():
            response = self.app.post('/orders', json={'user_id': 1, 'product_id': 1, 'quantity': 2})
        self.assertEqual(response.status_code, 201)
        self.assertIn('Order created successfully!', response.get_json()['message'])

    @patch('order_service.requests.get')
    def test_create_order_user_not_found(self, mock_get):
        """Test order creation when the user is not found."""
        # Mock the user service to return a 404 status
        mock_get.side_effect = [
            unittest.mock.Mock(status_code=404),  # User service returns 404
            unittest.mock.Mock(status_code=200, json=lambda: {'price': 150.00, 'stock': 10})  # Product service response
        ]
        
        # Simulate POST request to create an order
        with app.app_context():
            response = self.app.post('/orders', json={'user_id': 999, 'product_id': 1, 'quantity': 2})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json()['message'], 'User not found')

    @patch('order_service.requests.get')
    def test_create_order_product_not_found(self, mock_get):
        """Test order creation when the product is not found."""
        # Mock the user and product service responses
        mock_get.side_effect = [
            unittest.mock.Mock(status_code=200),  # User service response
            unittest.mock.Mock(status_code=404)   # Product service returns 404
        ]
        
        # Simulate POST request to create an order
        with app.app_context():
            response = self.app.post('/orders', json={'user_id': 1, 'product_id': 999, 'quantity': 2})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json()['message'], 'Product not found')

    @patch('order_service.requests.get')
    def test_create_order_insufficient_stock(self, mock_get):
        """Test order creation when there is insufficient stock."""
        # Mock the user and product service responses
        mock_get.side_effect = [
            unittest.mock.Mock(status_code=200),  # User service response
            unittest.mock.Mock(status_code=200, json=lambda: {'price': 150.00, 'stock': 1})  # Product service response with insufficient stock
        ]
        
        # Simulate POST request to create an order
        with app.app_context():
            response = self.app.post('/orders', json={'user_id': 1, 'product_id': 1, 'quantity': 2})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()['message'], 'Insufficient stock')

    def test_get_order_success(self):
        """Test getting an order by ID."""
        # Create an order in the test database within the app context
        with app.app_context():
            order = Order(user_id=1, product_id=1, quantity=2, total_price=300.00, status="Pending")
            db.session.add(order)
            db.session.commit()

            # Simulate GET request to fetch the order
            response = self.app.get(f'/orders/{order.id}')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json()['id'], order.id)


    def test_get_order_not_found(self):
        """Test getting an order by ID when the order does not exist."""
        # Simulate GET request for a non-existing order
        with app.app_context():
            response = self.app.get('/orders/9999')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json()['message'], 'Order not found')

    def test_load_predefined_orders(self):
        """Test loading predefined orders into the database."""
        # Simulate GET request to load predefined orders
        with app.app_context():
            response = self.app.get('/orders/all')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['message'], 'Predefined orders loaded successfully!')
        
        # Verify if orders were added to the database
        with app.app_context():
            orders = Order.query.all()
        self.assertEqual(len(orders), 3)  # Check if 3 predefined orders exist

if __name__ == '__main__':
    unittest.main()
