import os
import sys
import logging
from django.apps import AppConfig

logger = logging.getLogger('calisaas_logger')

class GymsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gyms'

    def ready(self):
        # Evitar ejecutar esto en comandos de migración o recarga automática de Django
        if 'runserver' not in sys.argv and 'gunicorn' not in os.environ.get('SERVER_SOFTWARE', ''):
            return

        # Para runserver, Django corre dos veces (una para el watcher). Solo queremos imprimirlo una vez.
        if os.environ.get('RUN_MAIN', None) == 'true':
            # 1. Prueba de Postgres
            try:
                from django.db import connection
                connection.ensure_connection()
                logger.info("✅ Conectado a Postgres exitosamente.")
            except Exception as e:
                logger.error(f"❌ Error conectando a Postgres: {e}")

            # 2. Prueba de Kafka
            try:
                from kafka import KafkaProducer
                from django.conf import settings
                # Intenta conectarse rápidamente con un timeout bajo para no bloquear el arranque
                producer = KafkaProducer(
                    bootstrap_servers=[settings.KAFKA_BROKER_URL],
                    api_version=(0, 10, 1),
                    request_timeout_ms=2000,
                    max_block_ms=2000
                )
                producer.close()
                logger.info("✅ Conectado a Kafka exitosamente.")
            except Exception as e:
                logger.error(f"❌ Error conectando a Kafka en {settings.KAFKA_BROKER_URL}: {e}")
