#!/bin/bash

# Replace this with your Coolify domain
DOMAIN="YOUR_COOLIFY_DOMAIN"

echo "Testing Rasa Deployment..."

echo -e "\n1. Checking Rasa server status..."
curl -s "https://$DOMAIN/status" | jq '.'

echo -e "\n2. Checking Actions server status..."
curl -s "https://$DOMAIN:5055/health"

echo -e "\n3. Testing basic conversation..."
echo "Sending: hello"
curl -s -X POST "https://$DOMAIN/webhooks/rest/webhook" \
  -H "Content-Type: application/json" \
  -d '{"message": "hello"}' | jq '.'

echo -e "\nSending: what time is it?"
curl -s -X POST "https://$DOMAIN/webhooks/rest/webhook" \
  -H "Content-Type: application/json" \
  -d '{"message": "what time is it?"}' | jq '.'

echo -e "\nSending: my name is John"
curl -s -X POST "https://$DOMAIN/webhooks/rest/webhook" \
  -H "Content-Type: application/json" \
  -d '{"message": "my name is John"}' | jq '.'

echo -e "\n4. Testing weather intent..."
curl -s -X POST "https://$DOMAIN/webhooks/rest/webhook" \
  -H "Content-Type: application/json" \
  -d '{"message": "what is the weather like?"}' | jq '.'

echo -e "\nTest complete!"
