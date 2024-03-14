import hvac
from typing import Text

client = hvac.Client(
    url='http://127.0.0.1:8200',
    token='',
)


def create_secret(key: Text, value: Text) -> None:
    client.secrets.kv.v2.create_or_update_secret(
        path=key,
        secret=dict(password=value),
    )


def rtrieve_secret(key: Text) -> Text:
    read_response = client.secrets.kv.read_secret_version(path=key)
    return read_response['data']['data']['password']


if __name__ == '__main__':
    create_secret('SERP_API_KEY', '')
    create_secret('GOOGLE_API_KEY', '')
    create_secret('GOOGLE_SEARCH_ENGINE_ID', '')
    create_secret('TELEGRAM_TOKEN', '')
    create_secret('VK_TOKEN', '')
