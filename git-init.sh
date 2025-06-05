#!/bin/bash
# Initialize Git repository and prepare for GitHub

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "Error: Git is not installed. Please install Git before continuing."
    exit 1
fi

# Initialize git repository if not already initialized
if [ ! -d ".git" ]; then
    echo "Initializing Git repository..."
    git init
    
    # Add all files
    git add .
    
    # Create initial commit
    git commit -m "Initial commit: YouTube Music Playlist Downloader"
    
    echo "Git repository initialized."
else
    echo "Git repository already initialized."
fi

# Instructions for pushing to GitHub
echo ""
echo "To push this repository to GitHub:"
echo "1. Create a new repository on GitHub (https://github.com/new)"
echo "2. Connect your local repository to GitHub:"
echo "   git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git"
echo "3. Push your changes to GitHub:"
echo "   git push -u origin main"
echo ""
echo "Remember to replace YOUR-USERNAME and YOUR-REPO-NAME with your actual GitHub username and repository name."
