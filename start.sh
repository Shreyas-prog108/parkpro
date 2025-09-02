#!/bin/bash
echo "Running database migrations..."
flask db upgrade
echo "Starting Gunicorn server..."
exec gunicorn --bind 0.0.0.0:5000 --workers 1 --timeout 120 app:app
