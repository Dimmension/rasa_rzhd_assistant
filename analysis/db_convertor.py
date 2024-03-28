"""Script for extracting useful data from rasa logs."""

import ast

import pandas as pd
import sqlalchemy

from utils import get_url_connection


def extract_requests(df: pd.DataFrame) -> pd.DataFrame:
    request_data = pd.DataFrame(columns=['input_channel', 'text'])

    for _, row in df.iterrows():
        # Предобработка строки в синтаксис python.
        row.data = (
            str(row.data)
            .replace('null', 'None')
            .replace('false', 'False')
            .replace('true', 'True')
        )

        # Преобразование строки в python словарь.
        rasa_data_col = ast.literal_eval(row.data)

        # Извлечение событий сообщений пользователя и бота.
        if (
            rasa_data_col['event'] in ('user', 'bot')
            and row.intent_name == 'request_search'
        ):
            request_data.loc[len(request_data.index)] = [
                rasa_data_col['input_channel']
                if rasa_data_col.get('input_channel')
                else None,
                rasa_data_col['text'],
            ]

    return request_data


if __name__ == '__main__':
    # Подключение к базе.
    url = get_url_connection()
    engine = sqlalchemy.create_engine(url, echo=True)

    # Запрос всей базы и сохранение в DataFrame.
    query = 'select * from events;'
    rasa_df = pd.read_sql_query(query, con=engine)

    request_data = extract_requests(rasa_df)
    intent_data = rasa_df.intent_name.dropna()

    # Сохранение в csv.
    intent_data.to_csv('intent_data.csv', index_label='id')
    request_data.to_csv('request_data.csv', index_label='id')
