import os
from datetime import datetime
import pandas as pd

from logger import get_logger
from google.cloud.storage import Client

logger = get_logger(__name__)
now = datetime.now()
directory = f"{now.strftime('%d-%m-%Y')}"


def create_client() -> Client:
    client = Client()
    return client


def write_to_gcp(file_name: str, df: pd.DataFrame, chunk_index: int):
    client = create_client()
    bucket_name = os.getenv("BUCKET")
    logger.info("publishing file: " + file_name)
    df_as_string = df.to_csv(sep=';', index=False)
    bucket = client.bucket(bucket_name=bucket_name)
    bucket.blob(f"{directory}/{file_name}_{chunk_index}.csv").upload_from_string(df_as_string)
    logger.info("publish success")
