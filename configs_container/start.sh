#!/bin/bash

# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn waapuro.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 &

# Start Nginx processes
echo Starting Nginx.
exec nginx -g "daemon off;"
