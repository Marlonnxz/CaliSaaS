import json
from django.core.management.base import BaseCommand
from django.conf import settings
from kafka import KafkaConsumer

class Command(BaseCommand):
    help = 'Inicia el suscriptor (Consumer) de Kafka para escuchar eventos del Gym'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Iniciando el Consumidor de Kafka para CaliSaaS..."))
        
        # En entornos de desarrollo esperar a que kafka inicie
        try:
            consumer = KafkaConsumer(
                'athlete_events', # Tópico al cual suscribirnos
                bootstrap_servers=settings.KAFKA_BROKER_URL,
                group_id='calisaas-group',
                value_deserializer=lambda m: json.loads(m.decode('utf-8'))
            )
            
            self.stdout.write(self.style.SUCCESS(f"¡Conectado a Kafka en {settings.KAFKA_BROKER_URL}! Escuchando 'athlete_events'..."))
            
            for message in consumer:
                event_data = message.value
                event_type = event_data.get("event")
                payload = event_data.get("payload", {})
                
                if event_type == "ATHLETE_CREATED":
                    self.stdout.write(
                        self.style.SUCCESS(f"📥 EVENTO RECIBIDO: Nuevo atleta creado.")
                    )
                    self.stdout.write(f" -> Nombre: {payload.get('first_name')} {payload.get('last_name')}")
                    self.stdout.write(f" -> ID: {payload.get('id')}")
                    self.stdout.write(self.style.WARNING(" [MOCK] Simulando el envío de correo de Bienvenida al Atleta...\n"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error conectando al broker Kafka: {str(e)}"))
