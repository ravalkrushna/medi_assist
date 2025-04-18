# Use official Python image (slim for smaller size)
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy all project files
COPY . .

# Upgrade pip and install dependencies in one layer to speed up caching
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Expose the port the service runs on
EXPOSE 5001

# Command to run the application
CMD ["python", "run.py"]
