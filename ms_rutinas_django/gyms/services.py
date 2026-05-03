import json
from kafka import KafkaProducer
from django.conf import settings
import logging
from datetime import datetime

logger = logging.getLogger('calisaas_logger')

def get_producer():
    try:
        producer = KafkaProducer(
            bootstrap_servers=[settings.KAFKA_BROKER_URL],
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        return producer
    except Exception as e:
        logger.error(f"Failed to connect to Kafka: {e}")
        return None

def publicar_evento_kafka(topic, evento):
    """
    Función genérica para publicar eventos en Kafka.
    Inyecta automáticamente un timestamp al evento.
    """
    producer = get_producer()
    if not producer:
        logger.warning(f"No se pudo enviar el evento al tópico {topic} porque no hay conexión con Kafka.")
        return
    
    # Inyectar timestamp automáticamente
    evento['timestamp'] = datetime.utcnow().isoformat() + "Z"
    
    try:
        producer.send(topic, value=evento)
        producer.flush()
        logger.info(f"Evento publicado en Kafka [{topic}]: {evento['event_type']}")
    except Exception as e:
        logger.error(f"Error publicando evento en Kafka [{topic}]: {e}")