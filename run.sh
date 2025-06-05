#!/bin/bash
# Script to build and run the YouTube Music Downloader

# Create downloads directory if it doesn't exist
if [ ! -d "./downloads" ]; then
    mkdir -p ./downloads
    echo "Created downloads directory"
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed or not in PATH. Please install Docker to continue."
    exit 1
fi
echo "Docker is installed"

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "Warning: Docker Compose is not installed. Falling back to Docker commands."
    
    # Build the Docker image
    echo "Building Docker image..."
    docker build -t ytm-downloader .
    
    # Ask user for playlist URL or file
    read -p "Do you want to use playlists.txt file or enter URLs directly? (file/urls): " choice
    
    if [ "$choice" = "file" ]; then
        # Check if playlists.txt exists and has content
        if [ ! -f "./playlists.txt" ] || [ ! -s "./playlists.txt" ] || ! grep -v '^\s*#' ./playlists.txt | grep -q -v '^\s*$'; then
            echo "Warning: playlists.txt file is empty or doesn't exist. Please add playlist URLs to it."
            exit 1
        fi
        
        # Run Docker container with playlists.txt
        echo "Running container with playlists.txt..."
        docker run -v "$(pwd)/downloads:/downloads" -v "$(pwd)/playlists.txt:/app/playlists.txt:ro" ytm-downloader -f /app/playlists.txt
    else
        # Get URLs from user
        read -p "Enter playlist URLs (separated by space): " urls
        
        if [ -z "$urls" ]; then
            echo "Error: No URLs provided."
            exit 1
        fi
        
        # Run Docker container with provided URLs
        echo "Running container with provided URLs..."
        docker run -v "$(pwd)/downloads:/downloads" ytm-downloader $urls
    fi
    
    exit 0
fi

# If we got here, Docker Compose is available
echo "Starting YouTube Music Downloader with Docker Compose..."

# Check if playlists.txt exists and has content
if [ ! -f "./playlists.txt" ] || [ ! -s "./playlists.txt" ] || ! grep -v '^\s*#' ./playlists.txt | grep -q -v '^\s*$'; then
    echo "Warning: playlists.txt file is empty or doesn't exist. Please add playlist URLs to it."
    
    # Ask if user wants to enter URLs now
    read -p "Do you want to enter URLs now? (y/n): " addUrls
    
    if [ "$addUrls" = "y" ]; then
        echo "Enter playlist URLs (one per line, press Ctrl+D to finish):"
        echo -e "\n# Added on $(date '+%Y-%m-%d')" >> ./playlists.txt
        while IFS= read -r line; do
            if [ ! -z "$line" ]; then
                echo "$line" >> ./playlists.txt
            fi
        done
        
        echo "URLs added to playlists.txt"
    else
        exit 1
    fi
fi

# Run with Docker Compose
docker-compose up --build

echo "Downloads completed. MP3 files are available in the 'downloads' folder."
