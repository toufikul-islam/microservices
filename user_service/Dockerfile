# Use the slim Python base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install system dependencies required for psycopg2 and other build tools
RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install Python dependencies
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the application code into the container
COPY . .

# Specify the command to run your application
CMD ["python", "user_service.py"]
