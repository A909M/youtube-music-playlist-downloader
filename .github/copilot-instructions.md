<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# YouTube Music Playlist Downloader

This project is a Python application that uses yt-dlp and FFmpeg to download YouTube Music playlists and convert them to MP3 format.

## Important Files

- `main.py`: Entry point of the application
- `src/downloader.py`: Core functionality for downloading and converting videos
- `Dockerfile`: Container definition using multi-stage builds
- `docker-compose.yml`: Docker Compose configuration for easier usage

## Development Considerations

- Maintain compatibility with yt-dlp's latest API
- Follow Docker best practices for security and efficiency
- Handle error cases gracefully, especially for unavailable videos
- Support both YouTube and YouTube Music URLs
- Consider rate limiting to avoid IP blocking
- Preserve metadata for music files

## Code Style

- Follow PEP 8 for Python code style
- Use type hints where appropriate
- Write descriptive docstrings for classes and functions
- Add comprehensive error handling
- Include logging for debugging purposes
