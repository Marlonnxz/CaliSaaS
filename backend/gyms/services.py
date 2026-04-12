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

def send_workout_logged_event(workout_log):
    """Evento analítico: Cuando un atleta registra un entrenamiento"""
    producer = get_producer()
    if not producer: return
    
    topic = 'workout_metrics'
    data = {
        'event_type': 'WORKOUT_LOGGED',
        'log_id': workout_log.id,
        'athlete_id': workout_log.athlete.id if hasattr(workout_log, 'athlete') else None,
        'duration_minutes': workout_log.duration_minutes if hasattr(workout_log, 'duration_minutes') else 0,
        'gym_id': workout_log.gym.id if hasattr(workout_log, 'gym') else None
    }
    
    try:
        producer.send(topic, value=data)
        producer.flush()
        logger.info(f"Published WORKOUT_LOGGED event for log {workout_log.id}")
    except Exception as e:
        logger.error(f"Failed to publish event: {e}")

def send_routine_created_event(routine):
    """Evento operativo: Cuando el instructor crea una nueva rutina"""
    producer = get_producer()
    if not producer: return
    
    topic = 'gym_updates'
    data = {
        'event_type': 'ROUTINE_CREATED',
        'routine_id': routine.id,
        'routine_name': routine.name,
        'gym_id': routine.gym.id if hasattr(routine, 'gym') else None
    }
    
    try:
        producer.send(topic, value=data)
        producer.flush()
        logger.info(f"Published ROUTINE_CREATED event for {routine.id}")
    except Exception as e:
        logger.error(f"Failed to publish event: {e}")