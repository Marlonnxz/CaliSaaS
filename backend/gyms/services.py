import json
from kafka import KafkaProducer
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

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

def send_athlete_created_event(athlete):
    producer = get_producer()
    if not producer:
        return
    
    topic = 'athlete_events'
    data = {
        'event_type': 'ATHLETE_CREATED',
        'athlete_id': athlete.id,
        'gym_id': athlete.gym.id,
        'first_name': athlete.first_name,
        'last_name': athlete.last_name,
        'timestamp': athlete.gym.created_at.isoformat() if hasattr(athlete.gym, 'created_at') else None
    }
    
    try:
        producer.send(topic, value=data)
        producer.flush()
        logger.info(f"Published ATHLETE_CREATED event for {athlete.id}")
    except Exception as e:
        logger.error(f"Failed to publish event to Kafka: {e}")
