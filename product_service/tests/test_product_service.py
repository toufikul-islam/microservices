import unittest
from product_service import app, db, Product

class ProductServiceTestCase(unittest.TestCase):
    def setUp(self):
        """Set up the test environment"""
        # Create a test client and set up an in-memory database
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_product_db.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app = app.test_client()
        self.app.testing = True
        
        # Create all the tables in the test database
        with app.app_context():
            db.create_all()

    def tearDown(self):
        """Clean up the database after each test"""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_product(self):
        """Test the product creation endpoint"""
        response = self.app.post('/products', json={
            'name': 'Laptop',
            'description': 'A high-end laptop',
            'price': 1200.00,
            'stock': 10
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('Product created successfully!', response.get_json()['message'])

    def test_get_product(self):
        """Test the endpoint for getting a product by ID"""
        # First, create a product
        self.app.post('/products', json={
            'name': 'Laptop',
            'description': 'A high-end laptop',
            'price': 1200.00,
            'stock': 10
        })

        # Now, get the product by ID
        response = self.app.get('/products/1')
        self.assertEqual(response.status_code, 200)
        product = response.get_json()
        self.assertEqual(product['name'], 'Laptop')
        self.assertEqual(product['description'], 'A high-end laptop')

    def test_get_product_not_found(self):
        """Test the case where a product is not found"""
        response = self.app.get('/products/999')  # Non-existing product ID
        self.assertEqual(response.status_code, 404)
        self.assertIn('Product not found', response.get_json()['message'])

    def test_load_predefined_products(self):
        """Test the loading of predefined products"""
        response = self.app.get('/products/all')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Predefined products loaded successfully!', response.get_json()['message'])

        # Check that predefined products were inserted into the database
        with app.app_context():
            products = Product.query.all()
            self.assertEqual(len(products), 3)  # We inserted 3 products in the load route

    def test_create_product_missing_fields(self):
        """Test the case where the product creation fails due to missing fields"""
        response = self.app.post('/products', json={
            'name': 'Laptop',
            'price': 1200.00,
            'stock': 10 
        })  # Missing 'description'
        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing required fields', response.get_json()['message'])


if __name__ == '__main__':
    unittest.main()
