FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create models directory with proper permissions
RUN mkdir -p /app/models && chown -R 1000:1000 /app/models

# Copy the rest of the application
COPY . .

# Make start script executable
RUN chmod +x start.sh

# Command to run the Rasa server
CMD ["./start.sh"]