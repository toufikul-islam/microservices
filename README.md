# E-commerce Microservices Application

This project is a simple e-commerce application built using microservices architecture. It includes three main services: User Service, Product Service, and Order Service. The application is containerized using Docker and orchestrated using Kubernetes. Monitoring and logging are handled using the ELK Stack.

## Table of Contents

- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Services](#services)
  - [User Service](#user-service)
  - [Product Service](#product-service)
  - [Order Service](#order-service)
  - [Payment Service](#payment-service)
  - [Notification Service](#notification-service)
  - [API Gateway](#api-gateway)
- [Monitoring and Logging](#monitoring-and-logging)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)



## Prerequisites

- Docker
- Kubernetes
- Python 3.9
- Flask
- NGINX
- ELK Stack (Elasticsearch, Logstash, Kibana)

## Installation

1. **Clone the repository:**

```sh
git clone https://github.com/toufikul-islam/microservices.git
cd microservices
```
## Build Docker Images:
```
docker build -t user_service:latest -f user_service/Dockerfile user_service/
docker build -t product_service:latest -f product_service/Dockerfile product_service/
docker build -t order_service:latest -f order_service/Dockerfile order_service/
docker build -t payment_service:latest -f order_service/Dockerfile payment_service/
docker build -t notification_service:latest -f order_service/Dockerfile notification_service/
docker build -t api_gateway:latest -f api_gateway/Dockerfile api_gateway/
```

## Unit Test
```
python -m unittest tests/test_user_service.py
python -m unittest tests/test_product_service.py
python -m unittest tests/test_order_service.py
python -m unittest tests/test_payment_service.py
python -m unittest tests/test_notification_service.py
```


## Set Up Monitoring and Logging:
```
kubectl apply -f kubernetes/prometheus_deployment.yaml
kubectl apply -f kubernetes/grafana_deployment.yaml
kubectl apply -f kubernetes/elk_deployment.yaml
```

## Usage
### Access the API Gateway
The API Gateway will be accessible at the external IP address provided by Kubernetes. You can use tools like `curl` or Postman to interact with the services.
### Example Requests

#### Create User
```bash
curl -X POST http://<api-gateway-ip>/users \
-H "Content-Type: application/json" \
-d '{"id": "1", "name": "John Doe"}'
```

