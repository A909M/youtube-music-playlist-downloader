# PowerShell script to build and run the YouTube Music Downloader

# Create downloads directory if it doesn't exist
if (-not (Test-Path -Path ".\downloads")) {
    New-Item -ItemType Directory -Path ".\downloads"
    Write-Host "Created downloads directory"
}

# Check if Docker is installed
try {
    docker --version | Out-Null
    Write-Host "Docker is installed"
} catch {
    Write-Host "Error: Docker is not installed or not in PATH. Please install Docker to continue." -ForegroundColor Red
    exit 1
}

# Check if docker-compose is installed
try {
    docker-compose --version | Out-Null
    Write-Host "Docker Compose is installed"
} catch {
    Write-Host "Warning: Docker Compose is not installed. Falling back to Docker commands." -ForegroundColor Yellow
    
    # Build the Docker image
    Write-Host "Building Docker image..." -ForegroundColor Cyan
    docker build -t ytm-downloader .
    
    # Ask user for playlist URL or file
    $choice = Read-Host "Do you want to use playlists.txt file or enter URLs directly? (file/urls)"
    
    if ($choice -eq "file") {
        # Check if playlists.txt exists and has content
        if (-not (Test-Path -Path ".\playlists.txt") -or ((Get-Content ".\playlists.txt" | Where-Object {$_ -notmatch "^\s*#" -and $_ -notmatch "^\s*$"}).Count -eq 0)) {
            Write-Host "Warning: playlists.txt file is empty or doesn't exist. Please add playlist URLs to it." -ForegroundColor Yellow
            exit 1
        }
        
        # Run Docker container with playlists.txt
        Write-Host "Running container with playlists.txt..." -ForegroundColor Cyan
        docker run -v "${PWD}\downloads:/downloads" -v "${PWD}\playlists.txt:/app/playlists.txt:ro" ytm-downloader -f /app/playlists.txt
    } else {
        # Get URLs from user
        $urls = Read-Host "Enter playlist URLs (separated by space)"
        
        if ([string]::IsNullOrWhiteSpace($urls)) {
            Write-Host "Error: No URLs provided." -ForegroundColor Red
            exit 1
        }
        
        # Run Docker container with provided URLs
        Write-Host "Running container with provided URLs..." -ForegroundColor Cyan
        docker run -v "${PWD}\downloads:/downloads" ytm-downloader $urls
    }
    
    exit 0
}

# If we got here, Docker Compose is available
Write-Host "Starting YouTube Music Downloader with Docker Compose..." -ForegroundColor Cyan

# Check if playlists.txt exists and has content
if (-not (Test-Path -Path ".\playlists.txt") -or ((Get-Content ".\playlists.txt" | Where-Object {$_ -notmatch "^\s*#" -and $_ -notmatch "^\s*$"}).Count -eq 0)) {
    Write-Host "Warning: playlists.txt file is empty or doesn't exist. Please add playlist URLs to it." -ForegroundColor Yellow
    
    # Ask if user wants to enter URLs now
    $addUrls = Read-Host "Do you want to enter URLs now? (y/n)"
    
    if ($addUrls -eq "y") {
        $urls = Read-Host "Enter playlist URLs (one per line, press Enter twice to finish)"
        
        # Write URLs to playlists.txt
        Add-Content -Path ".\playlists.txt" -Value "`n# Added on $(Get-Date -Format 'yyyy-MM-dd')"
        $urls -split "`n" | ForEach-Object {
            if (-not [string]::IsNullOrWhiteSpace($_)) {
                Add-Content -Path ".\playlists.txt" -Value $_
            }
        }
        
        Write-Host "URLs added to playlists.txt" -ForegroundColor Green
    } else {
        exit 1
    }
}

# Run with Docker Compose
docker-compose up --build

Write-Host "Downloads completed. MP3 files are available in the 'downloads' folder." -ForegroundColor Green
