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
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Dict, Text, Any, List

class ActionBookSeat(Action):
    def name(self) -> Text:
        return "action_book_seat"

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        name = tracker.get_slot("name")
        phone = tracker.get_slot("phone")
        seat_number = tracker.get_slot("seat_number")

        response = requests.post("http://127.0.0.1:8000/reserve/", json={
            "name": name,
            "phone": phone,
            "seat_number": seat_number
        })

        if response.status_code == 200:
            dispatcher.utter_message(text="Your reservation has been successfully made!")
        else:
            dispatcher.utter_message(text="Sorry, something went wrong with your reservation.")
        return []

class ActionCancelSeat(Action):
    def name(self) -> Text:
        return "action_cancel_seat"

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        seat_number = tracker.get_slot("seat_number")

        response = requests.delete(f"http://127.0.0.1:8000/cancel/{seat_number}")

        if response.status_code == 200:
            dispatcher.utter_message(text="Your reservation has been successfully canceled.")
        else:
            dispatcher.utter_message(text="Could not find the reservation to cancel.")
        return []
    
class ActionCheckReservationStatus(Action):
    def name(self) -> Text:
        return "action_check_reservation_status"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        seat_number = tracker.get_slot("seat_number")

        if not seat_number:
            dispatcher.utter_message(text="Please provide a seat number to check the reservation status.")
            return []

        response = requests.get(f"http://127.0.0.1:8000/reserve/{seat_number}")
        
        if response.status_code == 200:
            data = response.json()
            dispatcher.utter_message(
                text=f"The reservation for seat number {seat_number} is under the name of {data['name']}, phone: {data['phone']}."
            )
        elif response.status_code == 404:
            dispatcher.utter_message(text="No reservation found for the given seat number.")
        else:
            dispatcher.utter_message(text="Sorry, something went wrong while checking the reservation status.")

        return []

