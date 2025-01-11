#!/bin/bash

echo "Starting deployment..."

# Navigate to the project directory
cd ~/biltp2p/mafees_playlist

# Pull latest changes
echo "Pulling latest changes..."
git pull origin main

# Stop and remove existing containers
echo "Stopping existing containers..."
sudo docker-compose down

# Clean up Docker system
echo "Cleaning Docker system..."
sudo docker system prune -af
sudo docker volume prune -f

# Rebuild and start containers
echo "Building and starting containers..."
sudo docker-compose up -d --build

echo "Deployment complete!"

# Show container status
echo "Container status:"
sudo docker-compose ps

# Show logs
echo "Application logs:"
sudo docker-compose logs --tail=50 