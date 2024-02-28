import requests


def get_rasa_json(text: str) -> str:
    """Get response in JSON format from RASA and process it.

    Args:
        text (str): client request

    Returns:
        str: rasa text response
    """
    url = 'http://localhost:5005/webhooks/custom_connector/webhook'

    json_obj = {
        'text': text,
        'metadata': {},
    }
    
    rasa_response = requests.post(url, json=json_obj, timeout=5).json()
    
    try:
        answer = [rasa_response[line]['text'] for line in range(len(rasa_response))]
    except KeyError:
        answer = ['Произошла ошибка, попробуйте еще раз!']

    return '\n'.join(answer)
