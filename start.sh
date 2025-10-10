#!/bin/bash
echo "Starting Gunicorn server..."
exec gunicorn --bind 0.0.0.0:5000 --workers 1 --timeout 120 app:app