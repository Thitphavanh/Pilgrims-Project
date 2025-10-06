#!/bin/bash

# SSL Certificate Setup Script for pilgrimsventure.com
# This script sets up SSL certificates using Let's Encrypt

echo "Setting up SSL certificates for pilgrimsventure.com..."

# Step 1: Start containers without SSL first
echo "Starting containers with HTTP-only configuration..."
docker-compose -f docker-compose.prod.yml up -d

# Wait for containers to be ready
sleep 10

# Step 2: Get SSL certificates
echo "Requesting SSL certificates from Let's Encrypt..."
docker-compose -f docker-compose.prod.yml run --rm certbot \
  certonly --webroot \
  --webroot-path=/var/www/certbot \
  --email admin@pilgrimsventure.com \
  --agree-tos \
  --no-eff-email \
  -d pilgrimsventure.com \
  -d www.pilgrimsventure.com

# Step 3: Check if certificates were created
if [ -d "/var/lib/docker/volumes/pilgrims_certbot_certs/_data/live/pilgrimsventure.com" ]; then
    echo "SSL certificates obtained successfully!"

    # Step 4: Restart nginx to use SSL configuration
    echo "Restarting nginx with SSL configuration..."
    docker-compose -f docker-compose.prod.yml restart nginx

    echo "SSL setup complete! Your site should now be available at:"
    echo "https://pilgrimsventure.com"
    echo "https://www.pilgrimsventure.com"
else
    echo "Failed to obtain SSL certificates. Please check the logs."
    docker-compose -f docker-compose.prod.yml logs certbot
fi

# Step 5: Set up certificate renewal
echo "Setting up certificate auto-renewal..."
docker-compose -f docker-compose.prod.yml run --rm certbot \
  renew --dry-run

echo "SSL setup script completed!"