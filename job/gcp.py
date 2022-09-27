import pandas as pd

from logger import get_logger
from google.cloud.storage import Client

logger = get_logger(__name__)


def create_client() -> Client:
    client = Client()
    return client


def publish_dataframe_as_file(client: Client, bucket_name: str, df: pd.DataFrame, file_name: str):
    logger.info("publishing file: " + file_name)
    df_as_string = df.to_csv(sep=';', index=False)
    bucket = client.bucket(bucket_name=bucket_name)
    bucket.blob(file_name).upload_from_string(df_as_string)
    logger.info("publish success")


def write_to_gcp(name: str, df: pd.DataFrame):
    client = create_client()
    bucket_name = "pam-statistikk"
    publish_dataframe_as_file(client=client, bucket_name=bucket_name, df=df, file_name=name)
    # opretter mappe med dagens dato om den ikke eksisterer fra før
    # putter filen i mappen
