# PowerShell script to create necessary directories for the application

# Create directories
New-Item -ItemType Directory -Path "downloads" -Force | Out-Null
New-Item -ItemType Directory -Path "logs" -Force | Out-Null

# Copy config template if config doesn't exist
if (-not (Test-Path -Path "config.yml")) {
    Copy-Item -Path "config.yml.template" -Destination "config.yml"
    Write-Host "Created default config.yml file"
}

Write-Host "Created necessary directories:"
Write-Host "- downloads: For storing downloaded MP3 files"
Write-Host "- logs: For application logs"
Write-Host ""
Write-Host "You can now edit playlists.txt to add your YouTube Music playlist URLs"
Write-Host "Then run the application using Docker Compose: docker-compose up"
