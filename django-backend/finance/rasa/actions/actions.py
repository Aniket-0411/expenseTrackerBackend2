import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
# New lines to configure Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web_django.settings")
import django
django.setup()

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from finance.models import Finance
from asgiref.sync import sync_to_async



class ActionFetchFinanceData(Action):
    def name(self) -> Text:
        return "action_fetch_finance_data"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            transactions = await sync_to_async(lambda: list(Finance.objects.all()[:5]))()  # changed code
            data = "\n".join([str(record) for record in transactions])
            dispatcher.utter_message(text=f"Recent Transactions:\n{data}")
        except Exception as e:
            dispatcher.utter_message(text=f"Error retrieving data: {e}")
        return []
