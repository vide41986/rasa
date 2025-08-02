# Rasa Chatbot with OpenAI Integration

A production-ready conversational AI chatbot built with Rasa Open Source and enhanced with OpenAI GPT integration. Designed for easy deployment on Coolify or any Docker-compatible platform.

## Features

- **Rasa Framework**: Structured dialogue management with intents, entities, and stories
- **OpenAI Integration**: Fallback responses and enhanced AI capabilities using GPT-3.5-turbo
- **Custom Actions**: Weather information, time queries, and form handling
- **REST API**: Full HTTP API for integration with web and mobile applications
- **Docker Ready**: Containerized for easy deployment on Coolify
- **Production Ready**: Comprehensive error handling and logging

## Quick Start

### Prerequisites

- Docker and Docker Compose
- OpenAI API key

### Local Development

1. Clone the repository
2. Copy `.env.example` to `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

3. Build and run with Docker Compose:
   ```bash
   docker-compose up --build
   ```

4. The chatbot will be available at:
   - REST API: http://localhost:5005
   - Actions server: http://localhost:5055

### Testing the Bot

Send a POST request to test the bot:

```bash
curl -X POST http://localhost:5005/webhooks/rest/webhook \
  -H "Content-Type: application/json" \
  -d '{"sender": "test", "message": "hello"}'
```

## Deployment on Coolify

1. Create a new project in Coolify
2. Connect your Git repository
3. Set the following environment variables:
   - `OPENAI_API_KEY`: Your OpenAI API key

4. Coolify will automatically build and deploy using the provided Dockerfile

## API Endpoints

- `POST /webhooks/rest/webhook` - Send messages to the bot
- `GET /status` - Health check endpoint
- `GET /version` - Get Rasa version info
- `POST /model/train` - Train a new model
- `GET /conversations/{conversation_id}/tracker` - Get conversation state

## Customization

### Adding New Intents

1. Add examples to `data/nlu.yml`
2. Create stories in `data/stories.yml`
3. Add responses to `domain.yml`
4. Retrain the model: `docker-compose exec rasa rasa train`

### Custom Actions

Add new actions in `actions/actions.py` and update `domain.yml`:

```python
class ActionCustom(Action):
    def name(self) -> Text:
        return "action_custom"

    async def run(self, dispatcher, tracker, domain):
        # Your custom logic here
        dispatcher.utter_message(text="Custom response")
        return []
```

### OpenAI Configuration

Modify the OpenAI integration in `actions/actions.py`:
- Change model (e.g., gpt-4)
- Adjust temperature and max_tokens
- Customize system prompts

## Architecture

```
├── config.yml          # Rasa configuration
├── domain.yml          # Domain definition
├── data/               # Training data
│   ├── nlu.yml        # Intent examples
│   ├── stories.yml    # Conversation stories
│   └── rules.yml      # Conversation rules
├── actions/           # Custom actions
│   └── actions.py     # Python actions with OpenAI
├── models/            # Trained models
├── Dockerfile         # Docker configuration
└── docker-compose.yml # Multi-container setup
```

## Environment Variables

- `OPENAI_API_KEY` - Required: Your OpenAI API key
- `RASA_CORS_ORIGINS` - Optional: CORS origins (default: "*")
- `RASA_DEBUG` - Optional: Enable debug mode

## Troubleshooting

### Common Issues

1. **OpenAI API Error**: Ensure your API key is correct and has sufficient credits
2. **Model Training Failed**: Check training data format in `data/` directory
3. **Actions Server Connection**: Verify action server is running on port 5055

### Logs

View logs with Docker Compose:
```bash
docker-compose logs -f rasa
```

## Support

For issues and questions:
1. Check the logs for detailed error messages
2. Verify environment variables are set correctly
3. Ensure OpenAI API key has sufficient credits
4. Review Rasa documentation for advanced configuration

## License

This project is open source and available under the MIT License.