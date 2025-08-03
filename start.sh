#!/bin/bash
set -e

cd /app

echo "Training Rasa model..."
rasa train

echo "Starting Rasa server..."
exec rasa run \
    --enable-api \
    --cors "*" \
    --port 5005 \
    --debug \
    --endpoints endpoints.yml
