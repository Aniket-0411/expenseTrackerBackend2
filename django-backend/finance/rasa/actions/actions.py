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

api_key = os.environ.get("DEEPSEEK_API")

system_content = "You are a helpful personal finance assistant, you can answer questions about finance, transactions, and personal finance management. You have access to a database of transactions and can provide summaries, averages, and other financial insights. The currency is in USD."
keyword_intent={
    "recent transactions": ["recent", "last", "recent", "5", "last 5", "last five", "recent five", "recent 5", "last 5 transactions", "recent 5 transactions"],
    "total expenses": ["total", "expenditures", "total expenses", "total spending"],
    "total income": ["total", "earnings", "total income", "total earnings", "total revenue"],
    "average income": ["average", "mean", "average income", "mean income"],
    "average expense": ["average", "mean", "average expense", "mean expense"],
    "summary": ["summary", "overview", "report", "summarize", "summarize", "summary report", "overview report", "financial summary"],
}

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
                    {"role": "system", "content": system_content+"\n" + data},
                    {"role": "user", "content": input},
                    {"role": "assistant", "content": f"Recent conversation:\n{memory}"},
                ],
                stream=False
            )

            dispatcher.utter_message(text=f"\n{response.choices[0].message.content}")
        except Exception as e:
            dispatcher.utter_message(text=f"Error retrieving data: {e}")
        return []
    
    def queries(self, input, keyword_intent=keyword_intent):
        # Check if the input contains any of the keywords in keyword_intent, return the intent + the data

        for intent, keywords in keyword_intent.items():
            for keyword in keywords:
                if keyword in input:
                    if intent == "recent transactions":
                        transactions = Finance.objects.all().order_by("date")[:5]
                        if not transactions:
                            return "No recent transactions found."
                        return f"Recent transactions: {', '.join([str(record) for record in transactions])}"
                    elif intent == "total expenses":
                        total_expenses = Finance.objects.filter(type="Expense").aggregate(Sum("amount"))["amount__sum"]
                        return f"Total expenses: {total_expenses}"
                    elif intent == "total income":
                        total_income = Finance.objects.filter(type="Income").aggregate(Sum("amount"))["amount__sum"]
                        return f"Total income: {total_income}"
                    elif intent == "average income":
                        avg_income = Finance.objects.filter(type="Income").aggregate(Avg("amount"))["amount__avg"]
                        return f"Average income: {avg_income}"
                    elif intent == "average expense":
                        avg_expense = Finance.objects.filter(type="Expense").aggregate(Avg("amount"))["amount__avg"]
                        return f"Average expense: {avg_expense}"
                    elif intent == "summary":
                        total_expenses = Finance.objects.filter(type="Expense").aggregate(Sum("amount"))["amount__sum"]
                        total_income = Finance.objects.filter(type="Income").aggregate(Sum("amount"))["amount__sum"]
                        avg_income = Finance.objects.filter(type="Income").aggregate(Avg("amount"))["amount__avg"]
                        avg_expense = Finance.objects.filter(type="Expense").aggregate(Avg("amount"))["amount__avg"]
                        category_expenses = Finance.objects.filter(type="Expense").values("category").annotate(total=Sum("amount"))
                        category_income = Finance.objects.filter(type="Income").values("category").annotate(total=Sum("amount"))
                        return f"Total expenses: {total_expenses}\nTotal income: {total_income}\nAverage income: {avg_income}\nAverage expense: {avg_expense}\nCategory expenses: {category_expenses}\nCategory income: {category_income}"        
        records = Finance.objects.all().order_by("date")
        formatted = ", ".join(
            f"{r.date} | {r.type}: ${r.amount}" for r in records
        )
        return f"Here is all the user's finance data: {formatted}"



    def get_recent_chat_messages(self):
        # Fetch the last 5 messages from ChatMessage ordered by creation time
        messages = list(ChatMessage.objects.all().order_by("-created_at")[:20])
        # Reverse so the conversation is in chronological order
        messages.reverse()
        return "\n".join([f"{m.sender}: {m.message}" for m in messages])

