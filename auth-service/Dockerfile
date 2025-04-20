FROM python:3.10-slim

# Install PostgreSQL client
RUN apt-get update && apt-get install -y postgresql-client

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Make the script executable (Linux only)
RUN chmod +x wait-for-db.sh

CMD ["./wait-for-db.sh", "python", "app.py"]
