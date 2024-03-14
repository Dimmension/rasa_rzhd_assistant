import requests
from utils import config

from serpapi import search
from vault import vault_utils


SERP_API_KEY = vault_utils.rtrieve_secret('SERP_API_KEY')

GOOGLE_API_KEY = vault_utils.rtrieve_secret('GOOGLE_API_KEY')
GOOGLE_SEARCH_ENGINE_ID = vault_utils.rtrieve_secret('GOOGLE_SEARCH_ENGINE_ID')

serp_stats_params = {
    'api_key': SERP_API_KEY,
}

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


def _google_custom_search(request: str) -> str:
    """Search using Google Search and give helpful urls.

    Args:
        request (str): user request that need to be answered.

    Returns:
        str: list of urls or failure response
    """
    # Using Google Search API
    google_search_params['q'] = request
    response = requests.get(
        config.URL_GOOGLE_SEARCH, params=google_search_params, timeout=5,
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
    response = requests.get(
        config.URL_SERPAPI_STATS_PAGE, params=serp_stats_params, timeout=5,
    )
    search_results = response.json()
    requests_left = search_results['plan_searches_left']

    if request == '':
        return 'Вы ввели пустую строку!'

    if requests_left == 0:
        return _google_custom_search(request)

    # Enter client request to search engine
    serp_params['q'] = request
    # Get json response and convert to dict
    search_results = search(serp_params).as_dict()
    try:
        ans = search_results['related_questions'][0]['snippet']
        return f'Ответ на ваш запрос:{ans}'
    except KeyError:
        return _google_custom_search(request)
