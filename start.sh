#!/bin/bash
echo "Initializing database tables..."
python -c "from app import app, db; app.app_context().push(); db.create_all()"
echo "Starting Gunicorn server..."
exec gunicorn --bind 0.0.0.0:5000 --workers 1 --timeout 120 app:app