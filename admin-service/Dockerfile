FROM python:3.10-slim

# Install netcat-openbsd (correct version)
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your app
COPY . .

# Make the wait script executable
RUN chmod +x wait-for-db.sh

# Expose port
EXPOSE 5002

# FIXED CMD: Pass arguments to script correctly
CMD ["./wait-for-db.sh", "python app.py"]
