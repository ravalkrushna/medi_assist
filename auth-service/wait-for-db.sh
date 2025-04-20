#!/bin/sh

# Ensure the POSTGRES_USER environment variable is available
if [ -z "$POSTGRES_USER" ]; then
  echo "POSTGRES_USER is not set"
  exit 1
fi

# Wait for PostgreSQL to be ready
until pg_isready -h db -p 5432 -U $POSTGRES_USER; do
  echo "Waiting for PostgreSQL..."
  sleep 2
done

echo "PostgreSQL is ready!"
exec "$@"