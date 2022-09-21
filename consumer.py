import threading
import os
import uuid
import json
import traceback

from processors.processor import Processor
from api import API
from kafka3 import KafkaConsumer
from kafka3.errors import KafkaError, NoBrokersAvailable
from logger import get_logger


def create_consumer(topic: str, kafka_group_id: str, processor: Processor, api: API):
    return Consumer(
        topic=topic,
        kafka_brokers=os.environ["KAFKA_BROKERS"],
        kafka_ca_path=os.environ["KAFKA_CA_PATH"],
        ssl_certfile=os.environ["KAFKA_CERTIFICATE_PATH"],
        ssl_keyfile=os.environ["KAFKA_PRIVATE_KEY_PATH"],
        kafka_group_id=kafka_group_id,
        kafka_schema_registry=os.environ['KAFKA_SCHEMA_REGISTRY'],
        client_id=kafka_group_id + str(uuid.uuid4().int),
        api=api,
        processor=processor
    )


class Consumer:
    def __init__(self, api: API, processor: Processor, topic: str, kafka_brokers: str, kafka_ca_path: str, kafka_group_id: str,
                 kafka_schema_registry: str, client_id: str, ssl_certfile=None, ssl_keyfile=None,
                 ):
        self._logger = get_logger(__name__)
        self._schema_cache = {}
        self._schema_registry = kafka_schema_registry
        self._topic = topic
        self._kafka_brokers = kafka_brokers
        self.ssl_certfile = ssl_certfile
        self.ssl_keyfile = ssl_keyfile
        self._kafka_ca_path = kafka_ca_path
        self._kafka_group_id = kafka_group_id
        self._client_id = client_id
        self.api = api
        self.processor = processor

        self._logger.info("initiating consumer app")
        threading.Thread(target=self.read_topic, daemon=True).start()

    def read_topic(self):
        consumer = self.create_consumer()
        self._logger.info("Application is_ready OK")
        try:
            self._logger.info("readying kafka messages...")
            for msg in consumer:
                self.processor.process(msg)
                consumer.commit()

        except KafkaError as e:
            self._logger.error(f"Kafka-error - {e} - {traceback.format_exc()}")
            self.api.set_alive(False)
        except Exception as e:
            self._logger.error(f"ERROR - {e} - {traceback.format_exc()}")
            self.api.set_alive(False)

        self._logger.error("Kafka consumer stopped. Restarting app.")
        self.api.set_alive(False)

    def create_consumer(self) -> KafkaConsumer:
        try:
            consumer = KafkaConsumer(self._topic,
                                     bootstrap_servers=self._kafka_brokers,
                                     security_protocol='SSL',
                                     ssl_cafile=self._kafka_ca_path,
                                     ssl_certfile=self.ssl_certfile,
                                     ssl_keyfile=self.ssl_keyfile,
                                     value_deserializer=lambda x: json.loads(x.decode('utf-8')),
                                     auto_offset_reset="earliest",
                                     group_id=self._kafka_group_id,
                                     enable_auto_commit=False,
                                     api_version_auto_timeout_ms=20000,
                                     client_id=self._client_id
                                     )

            self._logger.info(f"Kafka consumer started OK: {consumer}, topic: {self._topic}")
        except NoBrokersAvailable:
            self._logger.error(f"Kafka initialization error for topic: {self._topic}. Restarting app.")
            self.api.set_alive(False)
        except Exception as e:
            self._logger.error(f"Kafka initialization error for topic: {self._topic}. Restarting app. {e}")
            self.api.set_alive(False)
        else:
            return consumer
