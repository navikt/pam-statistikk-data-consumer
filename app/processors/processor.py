from kafka3.consumer.fetcher import ConsumerRecord
from app.db.database import Database


class Processor:
    def __init__(self):
        self.db = None

    def process(self, msg: ConsumerRecord):
        pass

    def set_db_instance(self, db: Database):
        self.db = db

