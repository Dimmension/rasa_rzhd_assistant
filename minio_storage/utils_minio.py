"""Module that provides functions for interact with MiniIO storage."""
import os
from typing import Optional
from urllib.request import urlopen

from dotenv import load_dotenv
from minio import Minio

load_dotenv()

client = Minio(
    '127.0.0.1:9000',
    access_key=os.getenv('MINIO_USER'),
    secret_key=os.getenv('MINIO_PASSWORD'),
    secure=False,
)


def load_from_minio_first(
    bucket_name: str,
    local_filename: str,
    minio_filename: str,
) -> None:
    """Load file from local minio storage(first method).

    Args:
        bucket_name (str): bucket name on minio storage.
        local_filename (str): path to file you want to load.
        minio_filename (str): name that will be used as object name in minio.
    """
    try:
        response = client.get_object(bucket_name, minio_filename)
        with open(local_filename, 'wb') as file_data:
            for d in response.stream(32 * 1024):
                file_data.write(d)
    finally:
        response.close()
        response.release_conn()


def load_from_minio_second(
    bucket_name: str,
    local_filename: str,
    minio_filename: str,
) -> None:
    """Load file from local minio storage(second method).

    Args:
        bucket_name (str): bucket name on minio storage.
        local_filename (str): path to file you want to load.
        minio_filename (str): name that will be used as object name in minio.
    """
    client.fget_object(bucket_name, local_filename, minio_filename)


def load_to_minio(
    bucket_name: str,
    local_filename: Optional[str],
    minio_filename: str,
) -> None:
    """Load file to local minio storage.

    Args:
        bucket_name (str): bucket name on minio storage.
        local_filename (str): path to file you want to load.
        minio_filename (str): name that will be used as object name in minio.
    """
    # Load image (for example cat)
    load_data = urlopen('https://cataas.com/cat')
    client.put_object(
        bucket_name,
        minio_filename,
        load_data,
        length=-1,
        part_size=10 * 1024 * 1024,
    )


if __name__ == '__main__':
    bucket_name = ''
    local_filename = ''
    minio_filename = ''
    # load_from_minio_first()
    # load_from_minio_second()
    # load_to_minio()
