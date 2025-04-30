from openai import OpenAI
from asgiref.sync import sync_to_async
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Action, Tracker
from finance.models import ChatMessage

import django
import os
import sys
from dotenv import load_dotenv
load_dotenv()
api_key = os.environ.get("DEEPSEEK_API")


sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../../')))
# Configure Django settings if required
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web_django.settings")
django.setup()

# ...existing imports...

client = OpenAI(api_key=api_key,
                base_url="https://api.deepseek.com")


class ActionOpenSourceLLM(Action):
    def name(self) -> str:
        return "action_open_source_llm"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:
        try:
            # get input from user
            input = tracker.latest_message.get("text", "")

            memory = await sync_to_async(self.get_recent_chat_messages)()
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages= [
                    {"role": "system", "content": "You are a helpful personal finance assistant with conversation memory"},
                    {"role": "user", "content": input},
                    {"role": "assistant", "content": f"Recent conversation:\n{memory}"},
                ],
                stream=False
            )

            dispatcher.utter_message(text=f"\n{response.choices[0].message.content}")
        except Exception as e:
            dispatcher.utter_message(text=f"Error retrieving data: {e}")
        return []
    
    def get_recent_chat_messages(self):
        # Fetch the last 5 messages from ChatMessage ordered by creation time
        messages = list(ChatMessage.objects.all().order_by("-created_at")[:20])
        # Reverse so the conversation is in chronological order
        messages.reverse()
        return "\n".join([f"{m.sender}: {m.message}" for m in messages])
