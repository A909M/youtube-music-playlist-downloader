# Use a specific Python version for better reproducibility
FROM python:3.11-slim AS builder

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies, including ffmpeg
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create a non-root user for better security
RUN useradd -m appuser

# Create and set permissions for the download directory
RUN mkdir -p /downloads && chown -R appuser:appuser /downloads

# Multi-stage build for smaller final image
FROM python:3.11-slim AS runtime

# Install runtime dependencies only
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Create a non-root user
RUN useradd -m appuser

# Set working directory
WORKDIR /app

# Copy application code
COPY . .

# Create directories and set permissions
RUN mkdir -p /downloads /logs && chown -R appuser:appuser /downloads /logs

# Set default environment variables
ENV OUTPUT_DIR=/downloads \
    MP3_QUALITY=320k \
    RATE_LIMIT=0 \
    MAX_RETRIES=3 \
    VERBOSE=0 \
    LOG_FILE=/logs/ytm-downloader.log

# Switch to non-root user
USER appuser

# Run the application
ENTRYPOINT ["python", "main.py"]

# Default command (can be overridden)
CMD ["--help"]
