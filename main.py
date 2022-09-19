import os
import logging
import uuid

from consumer_app import ConsumerApp

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

logger = logging.getLogger(__name__)

try:
    app = ConsumerApp(
        topic="teampam.cv-endret-intern-v2",
        kafka_brokers=os.environ["KAFKA_BROKERS"],
        kafka_ca_path=os.environ["KAFKA_CA_PATH"],
        ssl_certfile=os.environ["KAFKA_CERTIFICATE_PATH"],
        ssl_keyfile=os.environ["KAFKA_PRIVATE_KEY_PATH"],
        kafka_group_id="statistikk-data-consumer-v1",
        kafka_schema_registry=os.environ['KAFKA_SCHEMA_REGISTRY'],
        client_id="pam-markedsinnsikt-datastory-consumer-" + str(uuid.uuid4().int)
    )

except Exception as e:
    print(f"Application error: {e}")
    logger.error("Application ended")
    logger.error(e)
