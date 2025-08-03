from typing import Any, Text, Dict, List
import logging
import os
import requests
from datetime import datetime
import pytz

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.types import DomainDict
import openai

class ActionGetTime(Action):
    def name(self) -> Text:
        return "action_get_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Get current time
        current_time = datetime.now().strftime("%I:%M %p")
        
        dispatcher.utter_message(text=f"The current time is {current_time}")
        
        return []

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

class ActionOpenAIResponse(Action):
    """Custom action to get response from OpenAI GPT"""

    def name(self) -> Text:
        return "action_openai_response"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        
        user_message = tracker.latest_message.get('text', '')
        
        try:
            # Get chat history for context
            conversation_history = []
            
            # Add recent messages for context
            for event in tracker.events[-10:]:  # Last 10 events
                if event.get('event') == 'user':
                    conversation_history.append({
                        "role": "user", 
                        "content": event.get('text', '')
                    })
                elif event.get('event') == 'bot':
                    conversation_history.append({
                        "role": "assistant", 
                        "content": event.get('text', '')
                    })
            
            # Add system message for context
            messages = [
                {
                    "role": "system", 
                    "content": "You are a helpful assistant integrated with a Rasa chatbot. Keep responses concise and friendly. If asked about capabilities, mention you're powered by Rasa and OpenAI."
                }
            ]
            
            # Add conversation history
            messages.extend(conversation_history)
            
            # Add current user message
            messages.append({"role": "user", "content": user_message})
            
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=150,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content.strip()
            dispatcher.utter_message(text=ai_response)
            
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            dispatcher.utter_message(
                text="I'm having trouble processing that right now. Please try again later."
            )
        
        return []

class ActionGetWeather(Action):
    """Custom action to get weather information"""

    def name(self) -> Text:
        return "action_get_weather"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        
        location = tracker.get_slot('location') or 'your location'
        
        # In a real implementation, you would call a weather API
        # For demo purposes, we'll use OpenAI to generate a weather response
        
        try:
            user_message = f"What's the weather like in {location}?"
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a weather assistant. Provide a realistic but fictional weather report for the requested location. Keep it brief and helpful."
                    },
                    {"role": "user", "content": user_message}
                ],
                max_tokens=100,
                temperature=0.7
            )
            
            weather_response = response.choices[0].message.content.strip()
            dispatcher.utter_message(text=weather_response)
            
        except Exception as e:
            logger.error(f"Weather API error: {str(e)}")
            dispatcher.utter_message(
                text=f"I'm unable to get weather information for {location} right now. Please try again later."
            )
        
        return []

class ActionGetTime(Action):
    """Custom action to get current time"""

    def name(self) -> Text:
        return "action_get_time"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        
        current_time = datetime.now().strftime("%H:%M:%S")
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        dispatcher.utter_message(
            text=f"The current time is {current_time} on {current_date}."
        )
        
        return []

class ValidateUserNameForm(FormValidationAction):
    """Validates the user_name_form"""

    def name(self) -> Text:
        return "validate_user_name_form"

    def validate_user_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate user_name value."""
        
        if len(slot_value) <= 2:
            dispatcher.utter_message(text="Please provide a name with more than 2 characters.")
            return {"user_name": None}
        else:
            return {"user_name": slot_value}