"""Module that provides utils for interaction with Postgres database."""

import os

from dotenv import load_dotenv


def get_url_connection() -> str:
    """Get a url to connect to the database.

    Returns:
        str: url with user credentials.
    """
    load_dotenv()
    env_vars = ['PG_USER', 'PG_PASSWORD', 'PG_HOST', 'PG_PORT', 'PG_DBNAME']
    user, password, host, port, dbname = [
        os.getenv(env_var) for env_var in env_vars
    ]
    return f'postgresql+psycopg://{user}:{password}@{host}:{port}/{dbname}'
