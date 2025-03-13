# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
import sqlite3
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# Helper function to execute queries


def execute_query(query: str, params: tuple = ()) -> List[tuple]:
    try:
        # Use a relative path to the database located in the project root
        with sqlite3.connect("../../mydb.db") as connection:
            cursor = connection.cursor()
            print("Connected to SQLite")
            cursor.execute(query, params)
            return cursor.fetchall()
    except Exception as e:
        return f"Error: {e}"


class ActionFetchFinanceData(Action):
    def name(self) -> Text:
        return "action_fetch_finance_data"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        query = "SELECT * FROM finance LIMIT 5;"
        result = execute_query(query)
        if isinstance(result, str):
            dispatcher.utter_message(text=f"Error retrieving data: {result}")
        else:
            result_text = "Recent Transactions:\n" + \
                "\n".join([str(row) for row in result])
            dispatcher.utter_message(text=result_text)
        return []


class ActionFetchFinanceSummary(Action):
    def name(self) -> Text:
        return "action_fetch_finance_summary"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        query = "SELECT type, SUM(amount) FROM finance GROUP BY type;"
        summary = execute_query(query)
        if isinstance(summary, str):
            dispatcher.utter_message(
                text=f"Error retrieving summary: {summary}")
        else:
            summary_text = "Finance Summary:\n" + \
                "\n".join([f"{row[0]}: {row[1]}" for row in summary])
            dispatcher.utter_message(text=summary_text)
        return []
