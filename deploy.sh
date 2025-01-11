#!/bin/bash

set -e  # Exit on error

echo "Starting deployment..."

# Navigate to the project directory
cd ~/biltp2p/mafees_playlist

# Pull latest changes
echo "Pulling latest changes..."
git pull origin main

# Stop and remove existing containers
echo "Stopping existing containers..."
sudo docker-compose down || true

# Clean up Docker system
echo "Cleaning Docker system..."
sudo docker system prune -af
sudo docker volume prune -f

# Remove any existing containers with the same names
echo "Removing existing containers..."
sudo docker rm -f mafees_playlist_redis mafees_playlist_app 2>/dev/null || true

# Rebuild and start containers
echo "Building and starting containers..."
sudo docker-compose up -d --build

# Wait for services to be healthy
echo "Waiting for services to be healthy..."
sleep 10

# Check container status
echo "Container status:"
sudo docker-compose ps

# Show logs if there are any errors
if [ "$(sudo docker-compose ps -q | wc -l)" -ne "2" ]; then
    echo "Error: Not all containers are running. Showing logs..."
    sudo docker-compose logs
    exit 1
fi

echo "Deployment complete! Services are running."

# Show recent logs
echo "Recent application logs:"
sudo docker-compose logs --tail=50 