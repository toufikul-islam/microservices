import unittest
import json
from payment_service import app, db, Payment

class PaymentServiceTestCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_payment_service.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app = app.test_client()
        self.app.testing = True

        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_process_payment(self):
        payment_data = {"order_id": 1, "user_id": 101, "amount": 100.50, "status": "completed"}
        response = self.app.post('/payments', data=json.dumps(payment_data), content_type='application/json')
        data = json.loads(response.data)

        print("Process Payment Response:", response.status_code, response.data.decode())  # Debugging
        self.assertEqual(response.status_code, 201)
        self.assertIn('payment_id', data)
        self.assertEqual(data['message'], "Payment processed successfully!")

    def test_get_payment_by_order(self):
        payment_data = {"order_id": 2, "user_id": 102, "amount": 200.75, "status": "pending"}
        self.app.post('/payments', data=json.dumps(payment_data), content_type='application/json')

        response = self.app.get('/payments/order/2')
        data = json.loads(response.data)

        print("Get Payment by Order Response:", response.status_code, response.data.decode())  # Debugging
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['order_id'], 2)
        self.assertEqual(data['user_id'], 102)
        self.assertEqual(data['amount'], 200.75)
        self.assertEqual(data['status'], 'pending')

    def test_update_payment_amount(self):
        payment_data = {"order_id": 3, "user_id": 103, "amount": 50.00, "status": "pending"}
        self.app.post('/payments', data=json.dumps(payment_data), content_type='application/json')

        update_data = {"amount": 75.00}
        response = self.app.put('/payments/order/3', data=json.dumps(update_data), content_type='application/json')
        data = json.loads(response.data)

        print("Update Payment Response:", response.status_code, response.data.decode())  # Debugging
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], "Payment updated successfully!")
        self.assertEqual(data['new_amount'], 75.00)

    def test_get_all_payments(self):
        self.app.post('/payments', data=json.dumps({"order_id": 4, "user_id": 104, "amount": 300.00, "status": "completed"}), content_type='application/json')
        self.app.post('/payments', data=json.dumps({"order_id": 5, "user_id": 105, "amount": 400.00, "status": "completed"}), content_type='application/json')

        response = self.app.get('/payments/all')
        data = json.loads(response.data)

        print("Get All Payments Response:", response.status_code, response.data.decode())  # Debugging
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 2)
        self.assertTrue(all('user_id' in payment for payment in data))

    # def test_delete_payment(self):
    #     payment_data = {"order_id": 6, "user_id": 106, "amount": 150.00, "status": "completed"}
    #     self.app.post('/payment', data=json.dumps(payment_data), content_type='application/json')

    #     response = self.app.delete('/payment/order/6')
    #     data = json.loads(response.data)

    #     print("Delete Payment Response:", response.status_code, response.data.decode())  # Debugging
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data['message'], "Payment for order 6 deleted successfully!")

    #     response = self.app.get('/payment/order/6')
    #     self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
