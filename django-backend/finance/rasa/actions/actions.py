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
from finance.models import Finance, ChatMessage
from asgiref.sync import sync_to_async
from openai import OpenAI
from django.db.models import Sum, Avg
from dotenv import load_dotenv
load_dotenv()

api_key = os.environ.get("deepseekAPI")


client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
class ActionFetchFinanceData(Action):
    def name(self) -> Text:
        return "action_fetch_finance_data"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            # get input from user
            input = tracker.latest_message.get("text", "")
            data = await sync_to_async(self.queries)(input)
            memory = await sync_to_async(self.get_recent_chat_messages)()
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages= [
                    {"role": "system", "content": "You are a helpful personal finance assistant with conversation memory"},
                    {"role": "user", "content": data},
                    {"role": "assistant", "content": f"Recent conversation:\n{memory}"},
                ],
                stream=False
            )

            dispatcher.utter_message(text=f"\n{response.choices[0].message.content}")
        except Exception as e:
            dispatcher.utter_message(text=f"Error retrieving data: {e}")
        return []
    
    def queries(self, input):
        if "recent" in input and "show" in input and "transactions" in input:
            transactions = Finance.objects.all()[:5]
            return "\n".join([str(record) for record in transactions])
        if "total" in input and "expenses" in input:
            total_expenses = Finance.objects.filter(type="Expense").aggregate(Sum("amount"))["amount__sum"]
            return f"Total expenses: {total_expenses}"
        if "total" in input and "income" in input:
            total_income = Finance.objects.filter(type="Income").aggregate(Sum("amount"))["amount__sum"]
            return f"Total income: {total_income}"
        if "average" in input and "income" in input:
            avg_income = Finance.objects.filter(type="Income").aggregate(Avg("amount"))["amount__avg"]
            return f"Average income: {avg_income}"
        if "average" in input and "expense" in input:
            avg_expense = Finance.objects.filter(type="Expense").aggregate(Avg("amount"))["amount__avg"]
            return f"Average expense: {avg_expense}"
        if "summary" in input or "overview" in input or "report" in input or "summarize" in input:
            total_expenses = Finance.objects.filter(type="Expense").aggregate(Sum("amount"))["amount__sum"]
            total_income = Finance.objects.filter(type="Income").aggregate(Sum("amount"))["amount__sum"]
            avg_income = Finance.objects.filter(type="Income").aggregate(Avg("amount"))["amount__avg"]
            avg_expense = Finance.objects.filter(type="Expense").aggregate(Avg("amount"))["amount__avg"]
            category_expenses = Finance.objects.filter(type="Expense").values("category").annotate(total=Sum("amount"))
            category_income = Finance.objects.filter(type="Income").values("category").annotate(total=Sum("amount"))
            return f"Total expenses: {total_expenses}\nTotal income: {total_income}\nAverage income: {avg_income}\nAverage expense: {avg_expense}\nCategory expenses: {category_expenses}\nCategory income: {category_income}"
        
    def get_recent_chat_messages(self):
        # Fetch the last 5 messages from ChatMessage ordered by creation time
        messages = list(ChatMessage.objects.all().order_by("-created_at")[:20])
        # Reverse so the conversation is in chronological order
        messages.reverse()
        return "\n".join([f"{m.sender}: {m.message}" for m in messages])

