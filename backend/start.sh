#!/bin/bash
source /var/www/dahouse-full/backend/env/bin/activate
exec gunicorn wsgi:app \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --threads 2 \
    --worker-class=gthread \
    --worker-connections=1000 \
    --keep-alive 5 \
    --max-requests 1000 \
    --max-requests-jitter 50 \
    --timeout 30