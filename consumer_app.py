import threading

from starlette.responses import JSONResponse
from fastapi import FastAPI
from starlette import status
from kafka3 import KafkaConsumer
from kafka3.errors import KafkaError, NoBrokersAvailable
from logger import get_logger


class ConsumerApp:
    def __init__(self, topic: str, kafka_brokers: str, kafka_ca_path: str, kafka_group_id: str,
                 kafka_schema_registry: str, client_id: str, ssl_certfile=None, ssl_keyfile=None):
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
        self._app = FastAPI()
        self._is_alive = True
        self._is_ready = False
        self.add_endpoints()

        self._logger.info("initiating consumer app")
        # threading.Thread(target=self.read_topic, daemon=True).start()

    @property
    def app(self):
        return self._app

    def read_topic(self):
        consumer = self.create_consumer()

        self._is_ready = True
        self._logger.info("Application is_ready OK")

        try:
            for msg in consumer:
                self._logger.info(msg)

                # consumer.commit()
        except KafkaError:
            self._is_alive = False

        self._logger.error("Kafka consumer stopped. Restarting app.")
        self._is_alive = False
        raise KafkaError()

    def healthiness(self):
        if self._is_alive:
            return JSONResponse(status_code=status.HTTP_200_OK, content={"Status": f"ok"})
        else:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"Status": f"Unhealthy"},
            )

    def readiness(self):
        if self._is_ready:
            return JSONResponse(status_code=status.HTTP_200_OK, content={"Status": f"ok"})
        else:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"Status": f"NotReady"},
            )

    def add_endpoints(self):

        self._app.add_api_route(path="/isalive", endpoint=self.healthiness)
        self._app.add_api_route(path="/isready", endpoint=self.readiness)

    def create_consumer(self) -> KafkaConsumer:
        try:
            consumer = KafkaConsumer(self._topic,
                                     bootstrap_servers=self._kafka_brokers,
                                     security_protocol='SSL',
                                     ssl_cafile=self._kafka_ca_path,
                                     ssl_certfile=self.ssl_certfile,
                                     ssl_keyfile=self.ssl_keyfile,
                                     auto_offset_reset="earliest",
                                     group_id=self._kafka_group_id,
                                     enable_auto_commit=False,
                                     api_version_auto_timeout_ms=20000,
                                     client_id=self._client_id
                                     )

            self._logger.info(f"Kafka consumer started OK: {consumer}")
        except NoBrokersAvailable:
            self._logger.error("Kafka initialization error. Restarting app.")
            self._is_alive = False
        except Exception as e:
            self._logger.error(e)
            self._is_alive = False
        else:
            return consumer
