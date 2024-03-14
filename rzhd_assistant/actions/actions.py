"""Module RASA that provides actions."""
from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from utils import search


class ActionRequestSearch(Action):
    """Represents an action for search client request."""

    def name(self) -> Text:
        """Getter of action name in RASA.

        Returns:
            Text: action name.
        """
        return 'action_request_search'

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        """Run an action script.

        Args:
            dispatcher (CollectingDispatcher): obj to generate responses \
                            to send back to the user.
            tracker (Tracker): obj to get access bot memory.
            domain (Dict[Text, Any]): _description_

        Returns:
            List[Dict[Text, Any]]: _description_
        """
        client_request = tracker.latest_message['text']
        full_answer = f'{search.get_answer(client_request)}'
        dispatcher.utter_message(text=full_answer)

        return [SlotSet(key='client_request', value=None)]
