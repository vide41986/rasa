#!/bin/bash

# Start action server in background
rasa run actions --port 5055 &

# Wait a moment for action server to start
sleep 30


# Start Rasa server
rasa run --model models/20250803-043322-dichotomic-photon.tar.gz --enable-api --cors "*" --port 5005
