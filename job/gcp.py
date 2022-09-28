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


def publish_dataframe_as_file(client: Client, bucket_name: str, df: pd.DataFrame, file_name: str):
    # opretter mappe med dagens dato om den ikke eksisterer fra før
    # putter filen i mappen
    logger.info("publishing file: " + file_name)
    df_as_string = df.to_csv(sep=';', index=False)
    bucket = client.bucket(bucket_name=bucket_name)
    bucket.blob(f"{directory}/{file_name}.csv").upload_from_string(df_as_string)
    logger.info("publish success")


def write_to_gcp(name: str, df: pd.DataFrame):
    client = create_client()
    bucket_name = "pam-statistikk"
    publish_dataframe_as_file(client=client, bucket_name=bucket_name, df=df, file_name=name)
