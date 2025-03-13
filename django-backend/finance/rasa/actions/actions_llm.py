from openai import OpenAI
from asgiref.sync import sync_to_async
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Action, Tracker
import django
import os
import sys
from dotenv import load_dotenv
load_dotenv()
api_key = os.environ.get("deepseekAPI")


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

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:
        user_input = tracker.latest_message.get("text", "")

        result = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful personal finance assistant"},
                {"role": "user", "content": user_input},
            ],
            stream=False
        )
        response = result.choices[0].message.content
        dispatcher.utter_message(text=response)
        return []
