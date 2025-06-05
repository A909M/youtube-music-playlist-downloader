#!/bin/bash
# Script to create necessary directories for the application

# Create directories
mkdir -p downloads logs

# Copy config template if config doesn't exist
if [ ! -f "config.yml" ]; then
  cp config.yml.template config.yml
  echo "Created default config.yml file"
fi

echo "Created necessary directories:"
echo "- downloads: For storing downloaded MP3 files"
echo "- logs: For application logs"
echo ""
echo "You can now edit playlists.txt to add your YouTube Music playlist URLs"
echo "Then run the application using Docker Compose: docker-compose up"
