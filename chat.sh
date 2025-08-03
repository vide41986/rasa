#!/bin/bash
while true; do
    echo -n "You: "
    read message
    if [ "$message" = "quit" ]; then
        break
    fi
    curl -s -X POST http://localhost:5005/webhooks/rest/webhook \
         -H "Content-Type: application/json" \
         -d "{\"message\": \"$message\"}" | jq -r '.[].text'
done
