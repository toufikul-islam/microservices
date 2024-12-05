# test_integration.py
import unittest
import requests

class IntegrationTestCase(unittest.TestCase):
    
    def test_create_order_with_payment_and_notification(self):
        # Create user (Service: user_service)
        user_response = requests.post('http://localhost:5001/users', json={'id': '1', 'name': 'John Doe'})
        self.assertEqual(user_response.status_code, 201)  # Expecting '201 Created'

        # Create product (Service: product_service)
        product_response = requests.post('http://localhost:5002/products', json={'id': '1', 'name': 'Laptop'})
        self.assertEqual(product_response.status_code, 201)  # Expecting '201 Created'

        # Create order (Service: order_service)
        order_response = requests.post('http://localhost:5003/orders', json={'user_id': '1', 'product_id': '1'})
        self.assertEqual(order_response.status_code, 201)  # Expecting '201 Created'

        # Process payment (Service: payment_service)
        payment_response = requests.post('http://localhost:5004/payments', json={
            'user_id': '1',
            'order_id': '1',
            'amount': 1000  # Assume price of the laptop is 1000
        })
        self.assertEqual(payment_response.status_code, 200)  # Expecting '200 OK'

        # Send notification (Service: notification_service)
        notification_response = requests.post('http://localhost:5005/notifications', json={
            'user_id': '1',
            'message': 'Your payment for Order 1 has been successfully processed.'
        })
        self.assertEqual(notification_response.status_code, 200)  # Expecting '200 OK'

if __name__ == '__main__':
    unittest.main()
