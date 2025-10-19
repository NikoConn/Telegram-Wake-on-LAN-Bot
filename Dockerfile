# Use Python 3.11 slim image for smaller size
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org --no-cache-dir -r requirements.txt

# Copy application files
COPY main.py .
COPY persistence.py .

# Create volume mount point for data persistence
VOLUME ["/app/data"]

# Set environment variable for data file location
ENV DATA_FILE=/app/data/mac_registry.json

# Run the bot
CMD ["python", "main.py"]
