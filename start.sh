#!/bin/bash

# Start action server in background
rasa run actions --port 5055 &

# Wait a moment for action server to start
sleep 5

# Start Rasa server
rasa run --enable-api --cors "*" --port 5005 --host 0.0.0.0