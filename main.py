#!/usr/bin/env python3
"""
Main entry point for the YouTube Music Playlist Downloader.

Copyright (c) 2025 YouTube Music Playlist Downloader Contributors
Licensed under the MIT License. See LICENSE file for details.
"""
import os
import sys
from src.downloader import YoutubePlaylistDownloader, setup_logging

def main():
    """
    Main function to parse arguments and start the download process.
    When run inside Docker, this will use predefined environment variables.
    """
    import argparse
    
    parser = argparse.ArgumentParser(description="Download YouTube Music playlists as MP3")
    parser.add_argument("urls", nargs="*", help="YouTube Music playlist URLs to download")
    parser.add_argument("-o", "--output-dir", 
                        default=os.environ.get("OUTPUT_DIR", "./downloads"),
                        help="Directory to save downloaded files (default: ./downloads)")
    parser.add_argument("-q", "--quality", 
                        default=os.environ.get("MP3_QUALITY", "320k"),
                        help="MP3 audio quality (default: 320k)")
    parser.add_argument("-f", "--file", 
                        help="Text file with playlist URLs (one per line)")
    parser.add_argument("-r", "--rate-limit", action="store_true",
                        default=os.environ.get("RATE_LIMIT", "0") == "1",
                        help="Enable rate limiting to avoid IP blocking")
    parser.add_argument("--retries", type=int, 
                        default=int(os.environ.get("MAX_RETRIES", "3")),
                        help="Number of retries for failed downloads (default: 3)")
    parser.add_argument("--log-file", 
                        default=os.environ.get("LOG_FILE", ""),
                        help="Save logs to a file in addition to console output")
    parser.add_argument("-v", "--verbose", action="store_true",
                        default=os.environ.get("VERBOSE", "0") == "1",
                        help="Enable verbose logging")
    
    args = parser.parse_args()
    setup_logging(args.verbose, args.log_file if args.log_file else None)
    
    # Get URLs from command line arguments and/or input file
    urls = args.urls
    if args.file:
        try:
            with open(args.file, 'r') as f:
                file_urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                urls.extend(file_urls)
        except Exception as e:
            print(f"Error reading URL file: {e}", file=sys.stderr)
            sys.exit(1)
    
    if not urls:
        print("No playlist URLs provided. Use --help for usage information.", file=sys.stderr)
        sys.exit(1)
    
    # Create downloader and start downloading
    downloader = YoutubePlaylistDownloader(
        output_dir=args.output_dir, 
        quality=args.quality,
        rate_limit=args.rate_limit,
        max_retries=args.retries
    )
    downloader.download_multiple_playlists(urls)

if __name__ == "__main__":
    main()
