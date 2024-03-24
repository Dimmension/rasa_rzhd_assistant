"""Script for extracting useful data from rasa logs."""

import ast

import pandas as pd
import sqlalchemy

from utils import get_connection


def _extract_intent(row):
    """Extract data about intent."""
    # Обработка и извлечние необходимых данных.
    if row.intent_name:
        intent_data.loc[len(intent_data.index)] = [row.intent_name]


def _extract_request(row):
    """Extract data about user and input channel."""
    # Предобработка строки в синтаксис python.
    row.data = str(row.data).replace('null', 'None')
    row.data = str(row.data).replace('false', 'False')
    row.data = str(row.data).replace('true', 'True')

    # Преобразование строки в python код словаря.
    rasa_data = ast.literal_eval(row.data)

    # Обработка и извлечние необходимых данных.
    if rasa_data['event'] in ('user', 'bot') and row.intent_name == 'request_search':
        request_data.loc[len(request_data.index)] = [
            rasa_data['input_channel'] if rasa_data.get('input_channel') else None,
            rasa_data['text'],
        ]


if __name__ == '__main__':
    # Подключение к базе.
    url = get_connection()
    engine = sqlalchemy.create_engine(url, echo=True)

    # Запрос всей базы и сохранение в DataFrame.
    query = 'select * from events;'
    rasa_df = pd.read_sql_query(query, con=engine)

    # Будующие csv таблицы.
    request_data = pd.DataFrame(columns=['input_channel', 'text'])
    intent_data = pd.DataFrame(columns=['intent_name'])

    # Проход построчно по таблице.
    rasa_df.apply(_extract_request, axis=1)
    rasa_df.apply(_extract_intent, axis=1)

    # Сохранение в csv.
    intent_data.to_csv('intent_data.csv', index_label='id')
    request_data.to_csv('request_data.csv', index_label='id')
