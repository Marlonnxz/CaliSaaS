import json
import logging
from django.core.management.base import BaseCommand
from django.conf import settings
from kafka import KafkaConsumer

logger = logging.getLogger('calisaas_logger')

class Command(BaseCommand):
    help = 'Inicia el suscriptor (Consumer) de Kafka para escuchar eventos de CaliSaaS'

    def handle(self, *args, **options):
        logger.info("Iniciando el Consumidor de Kafka para CaliSaaS...")
        
        try:
            consumer = KafkaConsumer(
                'athlete_events',    # Tópico 1
                'workout_metrics',   # Tópico 2
                'gym_updates',       # Tópico 3
                bootstrap_servers=settings.KAFKA_BROKER_URL,
                group_id='calisaas-group',
                value_deserializer=lambda m: json.loads(m.decode('utf-8'))
            )
            
            logger.info(f"¡Conectado a Kafka en {settings.KAFKA_BROKER_URL}!")
            logger.info("Escuchando eventos en tiempo real...")
            
            for message in consumer:
                event_data = message.value
                event_type = event_data.get("event_type") # Corregido
                topic = message.topic
                
                logger.info(f"\n📥 [NUEVO MENSAJE EN TÓPICO: {topic}]")
                
                if event_type == "ATHLETE_CREATED":
                    logger.info(" -> Acción: Nuevo atleta creado.")
                    logger.info(f" -> Nombre: {event_data.get('first_name')} {event_data.get('last_name')}")
                    logger.warning(" -> [MOCK] Simulando el envío de correo de Bienvenida al Atleta...")
                
                elif event_type == "WORKOUT_LOGGED":
                    logger.info(" -> Acción: Entrenamiento registrado.")
                    logger.info(f" -> Log ID: {event_data.get('log_id')} | Duración: {event_data.get('duration_minutes')} min")
                    logger.warning(" -> [MOCK] Actualizando métricas del dashboard...")

                elif event_type == "ROUTINE_CREATED":
                    logger.info(" -> Acción: Nueva rutina publicada.")
                    logger.info(f" -> Rutina: {event_data.get('routine_name')}")
                    logger.warning(" -> [MOCK] Enviando notificación push a los atletas del gimnasio...")

        except Exception as e:
            logger.error(f"Error conectando al broker Kafka: {str(e)}")