#!/usr/bin/env python3
"""
YouTube Music Playlist Downloader
--------------------------------
Downloads playlists from YouTube Music and converts them to MP3 format.
"""
import os
import sys
import time
import argparse
import logging
import random
from typing import List, Optional, Dict, Any, Callable

import yt_dlp


class YoutubePlaylistDownloader:
    """Downloads YouTube Music playlists as MP3 files."""
    
    def __init__(self, output_dir: str = "./downloads", quality: str = "320k", 
                 rate_limit: bool = False, max_retries: int = 3, 
                 retry_sleep: int = 10):
        """
        Initialize the downloader with configuration options.
        
        Args:
            output_dir: Directory where downloaded files will be saved
            quality: Audio quality for MP3 conversion (e.g., "320k")
            rate_limit: If True, adds random delays between downloads to avoid blocking
            max_retries: Maximum number of retry attempts for failed downloads
            retry_sleep: Seconds to wait between retries
        """
        self.output_dir = output_dir
        self.quality = quality
        self.rate_limit = rate_limit
        self.max_retries = max_retries
        self.retry_sleep = retry_sleep
        self.logger = logging.getLogger("ytm-downloader")
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
    
    def _get_ydl_opts(self, playlist_title: Optional[str] = None) -> dict:
        """
        Configure yt-dlp options.
        
        Args:
            playlist_title: If provided, files will be organized in a subfolder
            
        Returns:
            Dictionary of yt-dlp options
        """
        # Base output template
        if playlist_title:
            # Create a folder for the playlist and include track number
            outtmpl = os.path.join(
                self.output_dir,
                f"{playlist_title}",
                "%(playlist_index)s - %(title)s.%(ext)s"
            )
        else:
            # Just use the title if not part of a playlist
            outtmpl = os.path.join(self.output_dir, "%(title)s.%(ext)s")
        
        # Progress hook for displaying download progress
        def progress_hook(d: Dict[str, Any]) -> None:
            if d['status'] == 'downloading':
                if '_percent_str' in d and '_eta_str' in d:
                    self.logger.info(f"Downloading: {d.get('filename', '')} - {d.get('_percent_str', '')} (ETA: {d.get('_eta_str', '')})")
            elif d['status'] == 'finished':
                self.logger.info(f"Downloaded: {d.get('filename', '')} - Converting to MP3...")
            elif d['status'] == 'error':
                self.logger.error(f"Error downloading: {d.get('filename', '')}")
        
        return {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': self.quality,
            }, {
                'key': 'FFmpegMetadata',
                'add_metadata': True,
            }, {
                'key': 'EmbedThumbnail',
            }],
            'outtmpl': outtmpl,
            'verbose': False,
            'quiet': False,
            'no_warnings': False,
            'ignoreerrors': True,  # Skip unavailable videos
            'geo_bypass': True,
            'extract_flat': False,
            'writethumbnail': True,
            'logger': self.logger,
            'progress_hooks': [progress_hook],
            'noprogress': False,
            # Network settings
            'socket_timeout': 30,  # Timeout for network operations
            'retries': 10,  # Internal retries for yt-dlp
            'fragment_retries': 10,  # Retry for ts/m3u8 fragments
            'skip_unavailable_fragments': True,  # Skip unavailable fragments
            'overwrites': True,  # Overwrite files if they exist
        }
    
    def _with_retry(self, func: Callable, *args, **kwargs) -> Any:
        """
        Execute a function with retry logic for network errors.
        
        Args:
            func: Function to execute
            *args: Positional arguments to pass to the function
            **kwargs: Keyword arguments to pass to the function
            
        Returns:
            Result of the function call
            
        Raises:
            Exception: If all retries fail
        """
        last_error = None
        for attempt in range(self.max_retries):
            try:
                return func(*args, **kwargs)
            except (yt_dlp.utils.DownloadError, yt_dlp.utils.ExtractorError) as e:
                # Check for specific network-related errors
                error_str = str(e).lower()
                if any(err in error_str for err in ['timeout', 'connection', 'network', 'reset', 'socket', 'ssl']):
                    self.logger.warning(f"Network error (attempt {attempt+1}/{self.max_retries}): {str(e)}")
                    last_error = e
                    time.sleep(self.retry_sleep * (attempt + 1))  # Exponential backoff
                else:
                    # Re-raise non-network errors
                    raise
        
        # If we get here, all retries failed
        raise last_error or Exception("All retry attempts failed")
    
    def _apply_rate_limit(self) -> None:
        """Apply rate limiting to avoid IP blocking."""
        if self.rate_limit:
            delay = random.uniform(1.0, 5.0)
            self.logger.debug(f"Rate limiting: sleeping for {delay:.2f} seconds")
            time.sleep(delay)
    
    def download_playlist(self, playlist_url: str) -> None:
        """
        Download all songs from a YouTube Music playlist.
        
        Args:
            playlist_url: URL to the YouTube Music playlist
        """
        self.logger.info(f"Downloading playlist: {playlist_url}")
        
        # First extract playlist info to get the title
        try:
            with yt_dlp.YoutubeDL({'extract_flat': True, 'quiet': True}) as ydl:
                playlist_info = self._with_retry(ydl.extract_info, playlist_url, download=False)
                playlist_title = playlist_info.get('title', 'Unknown_Playlist')
                playlist_title = playlist_title.replace('/', '_').replace('\\', '_')
                
                entries = playlist_info.get('entries', [])
                entry_count = len(entries)
                self.logger.info(f"Found playlist: {playlist_title} with {entry_count} videos")
                
                if entry_count == 0:
                    self.logger.warning(f"Playlist {playlist_url} appears to be empty or inaccessible")
                    return
        except Exception as e:
            self.logger.error(f"Failed to fetch playlist info: {str(e)}")
            return
        
        # Create output directory for this playlist
        playlist_dir = os.path.join(self.output_dir, playlist_title)
        os.makedirs(playlist_dir, exist_ok=True)
        
        # Now download with the playlist title included in the path
        try:
            with yt_dlp.YoutubeDL(self._get_ydl_opts(playlist_title)) as ydl:
                self._with_retry(ydl.download, [playlist_url])
                
            self.logger.info(f"Download complete. Files saved to {playlist_dir}")
        except Exception as e:
            self.logger.error(f"Error downloading playlist {playlist_url}: {str(e)}")
        finally:
            self._apply_rate_limit()
    
    def download_multiple_playlists(self, playlist_urls: List[str]) -> None:
        """
        Download multiple playlists.
        
        Args:
            playlist_urls: List of YouTube Music playlist URLs
        """
        total = len(playlist_urls)
        for i, url in enumerate(playlist_urls, 1):
            self.logger.info(f"Processing playlist {i}/{total}: {url}")
            try:
                self.download_playlist(url)
            except Exception as e:
                self.logger.error(f"Failed to download playlist {url}: {str(e)}")


def setup_logging(verbose: bool = False, log_file: Optional[str] = None) -> None:
    """
    Configure logging based on verbosity level.
    
    Args:
        verbose: If True, set log level to DEBUG, otherwise INFO
        log_file: If provided, also log to this file
    """
    log_level = logging.DEBUG if verbose else logging.INFO
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    
    handlers = [logging.StreamHandler()]
    if log_file:
        handlers.append(logging.FileHandler(log_file))
    
    logging.basicConfig(level=log_level, format=log_format, handlers=handlers)


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description="Download YouTube Music playlists as MP3")
    parser.add_argument("urls", nargs="+", help="YouTube Music playlist URLs to download")
    parser.add_argument("-o", "--output-dir", default="./downloads", 
                        help="Directory to save downloaded files (default: ./downloads)")
    parser.add_argument("-q", "--quality", default="320k",
                        help="MP3 audio quality (default: 320k)")
    parser.add_argument("-r", "--rate-limit", action="store_true",
                        help="Enable rate limiting to avoid IP blocking")
    parser.add_argument("--retries", type=int, default=3,
                        help="Number of retries for failed downloads (default: 3)")
    parser.add_argument("--log-file", 
                        help="Save logs to a file in addition to console output")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Enable verbose logging")
    
    args = parser.parse_args()
    setup_logging(args.verbose, args.log_file)
    
    downloader = YoutubePlaylistDownloader(
        output_dir=args.output_dir, 
        quality=args.quality,
        rate_limit=args.rate_limit,
        max_retries=args.retries
    )
    downloader.download_multiple_playlists(args.urls)


if __name__ == "__main__":
    main()
