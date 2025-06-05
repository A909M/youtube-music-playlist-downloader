# YouTube Music Playlist Downloader

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://www.docker.com/)

A Docker-based tool to download playlists from YouTube Music and convert them to MP3 format.

## Features

- Download entire playlists from YouTube Music
- Convert videos to high-quality MP3 files
- Preserve metadata (title, artist, album)
- Embed album artwork
- Organize downloads by playlist
- Support for multiple playlists
- Network error handling with retries
- Download progress tracking
- Rate limiting to avoid IP blocking
- Comprehensive logging

## Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/) (optional, but recommended)

## Quick Start

1. Clone this repository or download the files
2. Run the setup script to create necessary directories:

   ```bash
   # On Linux/Mac
   chmod +x setup.sh
   ./setup.sh

   # On Windows
   .\setup.ps1
   ```

3. Edit the `playlists.txt` file to add your YouTube Music playlist URLs (one per line)
4. Run the container using Docker Compose:
   ```bash
   docker-compose up
   ```

The downloaded MP3 files will be available in the `./downloads` directory, and logs in the `./logs` directory.

## Usage Options

### Using Docker Compose (recommended)

1. Edit the `playlists.txt` file with your playlist URLs
2. Run the container:

```bash
docker-compose up
```

To customize the MP3 quality:

```bash
MP3_QUALITY=192k docker-compose up
```

To enable rate limiting and add verbosity:

```bash
RATE_LIMIT=1 VERBOSE=1 docker-compose up
```

To specify additional arguments:

```bash
EXTRA_ARGS="--retries 5" docker-compose up
```

### Configuration File

The application also supports a YAML configuration file. By default, it looks for `config.yml` in the application directory.

Example configuration:

```yaml
# Output directory for downloaded files
output_dir: /downloads

# MP3 audio quality (e.g., 128k, 192k, 320k)
quality: 320k

# Enable rate limiting to avoid IP blocking (0=disabled, 1=enabled)
rate_limit: 0

# Maximum number of retries for failed downloads
max_retries: 3

# Log file path (leave empty for console-only logging)
log_file: /logs/ytm-downloader.log

# Verbose logging (0=normal, 1=verbose)
verbose: 0
```

To use a custom configuration file:

```bash
CONFIG_FILE=./my-custom-config.yml docker-compose up
```

### Using Docker directly

```bash
# Build the Docker image
docker build -t ytm-downloader .

# Download a single playlist
docker run -v "$(pwd)/downloads:/downloads" ytm-downloader "https://music.youtube.com/playlist?list=PLXXXXX"

# Download multiple playlists
docker run -v "$(pwd)/downloads:/downloads" ytm-downloader "https://music.youtube.com/playlist?list=PLXXXX" "https://music.youtube.com/playlist?list=PLyyyy"

# Download playlists from a file
docker run -v "$(pwd)/downloads:/downloads" -v "$(pwd)/playlists.txt:/app/playlists.txt:ro" ytm-downloader -f /app/playlists.txt
```

### Command-line Options

```bash
Usage: python main.py [OPTIONS] [URLS...]

Options:
  -o, --output-dir DIR     Directory to save downloaded files (default: ./downloads)
  -q, --quality QUALITY    MP3 audio quality (default: 320k)
  -f, --file FILE          Text file with playlist URLs (one per line)
  -r, --rate-limit         Enable rate limiting to avoid IP blocking
  --retries NUM            Number of retries for failed downloads (default: 3)
  --log-file FILE          Save logs to a file in addition to console output
  -v, --verbose            Enable verbose logging
  --help                   Show this help message
```

## Docker Image Details

The Docker image follows best practices:

- Uses multi-stage builds to reduce image size
- Runs as a non-root user for security
- Includes only necessary dependencies
- Uses specific version tags for reproducibility
- Properly handles signals for graceful shutdown

## License

MIT

## Acknowledgements

This tool uses:

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for downloading videos
- [FFmpeg](https://ffmpeg.org/) for audio conversion

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute to this project.

## GitHub Integration

This project is hosted on GitHub and includes CI/CD through GitHub Actions:

1. **Fork the Repository**: Fork this repository to your GitHub account
2. **Clone**: `git clone https://github.com/yourusername/youtube-music-downloader.git`
3. **Install Dependencies**: Run the setup script to prepare your environment
4. **Make Changes**: Implement your feature or fix
5. **Create a Pull Request**: Submit your changes for review

### GitHub Actions

The repository includes a GitHub Actions workflow that:

- Builds the Docker image
- Runs linting with flake8
- Tests the Docker container functionality
- Verifies directory structure

## Built With

This project was developed with the assistance of GitHub Copilot, an AI pair programming tool that helps generate code and provide suggestions during development.
