#!/bin/bash

# Display a message while creating the virtual environment
echo "🚀 Setting up a virtual environment..."
python -m venv venv
source venv/bin/activate

# Display a message while building the Docker image
echo "🐳 Building the Docker image for Django Auth Service..."
docker build -t django-auth-service .

# Display a message while running the Docker container
echo "🏃‍♂️ Running the Django Auth Service container in detached mode, mapping port 8000..."
docker run -d -p 8000:8000 django-auth-service
