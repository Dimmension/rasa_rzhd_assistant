"""Module RASA that provides actions."""
import json
import os
import requests

from typing import Any, Dict, List, Text
from urllib.request import urlopen

from dotenv import load_dotenv
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from serpapi import search

load_dotenv()

SERP_API_KEY = os.getenv('SERP_API_KEY')
URL_SERPAPI_STATS_PAGE = os.getenv('URL_SERPAPI_STATS_PAGE')

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
GOOGLE_SEARCH_ENGINE_ID = os.getenv('GOOGLE_SEARCH_ENGINE_ID')
URL_GOOGLE_SEARCH = os.getenv('URL_GOOGLE_SEARCH')

serp_params = {
    'engine': 'google',
    'q': None,
    'gl': 'ru',
    'lr': 'lang_ru',
    'api_key': SERP_API_KEY,
}

google_search_params = {
    'q': None,
    'key': GOOGLE_API_KEY,
    'cx': GOOGLE_SEARCH_ENGINE_ID,
    'hl': 'ru',
    'gl': 'ru',
}


def google_custom_search(request: str) -> str:
    """Search using Google Search and give helpful urls.

    Args:
        request (str): user request that need to be answered.

    Returns:
        str: list of urls or failure response
    """
    # Using Google Search API
    google_search_params['q'] = request
    response = requests.get(
        URL_GOOGLE_SEARCH, params=google_search_params, timeout=5,
    )
    # Google JSON response
    search_results = response.json()
    # Final list of links
    helpful_urls = []
    wiki = None
    # Collect helpful urls
    # Also can change number of collected links
    for ind in range(5):
        try:
            link = search_results['items'][ind]['link']
        except KeyError:
            link = None

        if link:
            if link.find('wikipedia') == -1:
                helpful_urls.append(link)
            else:
                wiki = link
    # Making Wikipedia our first priority
    if wiki:
        helpful_urls.insert(0, wiki)
    # Check for find any link
    if helpful_urls:
        if len(helpful_urls) > 3:
            helpful_urls = helpful_urls[:3]
        links = '\n-> '.join(helpful_urls)
        return f'\nВот ресурсы, которые могут вам дать ответ:\n-> {links}'

    return 'Ничего не удалось найти по вашему запросу.'


def get_answer(request: str) -> str:
    """Search user request with SerpApi in Google and take related_answer.

    Args:
        request (str): user request that need to be answered.

    Returns:
        str: answer that was recieved by searching in Google.
    """
    # Get count of left requests in SerpApi
    with urlopen(f'{URL_SERPAPI_STATS_PAGE}{SERP_API_KEY}') as url:
        json_raw = json.load(url)
        requests_left = json_raw['plan_searches_left']

    if request == '':
        return 'Вы ввели пустую строку!'

    if requests_left == 0:
        return google_custom_search(request)

    # Enter client request to search engine
    serp_params['q'] = request
    # Get json response and convert to dict
    search_results = search(serp_params).as_dict()
    try:
        ans = search_results['related_questions'][0]['snippet']
        return f'Ответ на ваш запрос:{ans}'
    except KeyError:
        return google_custom_search(request)


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
            dispatcher (CollectingDispatcher): obj to generate responses to send back to the user.
            tracker (Tracker): obj to get access bot memory.
            domain (Dict[Text, Any]): _description_

        Returns:
            List[Dict[Text, Any]]: _description_
        """
        client_request = tracker.latest_message['text']
        full_answer = f'{get_answer(client_request)}'
        dispatcher.utter_message(text=full_answer)

        return [SlotSet(key='client_request', value=None)]
