const { Kafka } = require('kafkajs');
const fs = require('fs');
const path = require('path');

const kafka = new Kafka({
  clientId: 'auditoria-consumer',
  brokers: [process.env.KAFKA_BROKER || 'localhost:9092']
});

const consumer = kafka.consumer({ groupId: 'auditoria-group' });
const logFilePath = path.join(__dirname, 'auditoria.log');

const run = async () => {
  await consumer.connect();
  console.log('Auditoria consumer connected to Kafka successfully');
  await consumer.subscribe({ topic: 'auditoria.gyms', fromBeginning: true });

  await consumer.run({
    eachMessage: async ({ topic, partition, message }) => {
      const eventValue = message.value.toString();
      console.log(`[AUDITORIA] Evento recibido: ${eventValue}`);
      
      const logEntry = `[${new Date().toISOString()}] ${eventValue}\n`;
      fs.appendFileSync(logFilePath, logEntry);
    },
  });
};

run().catch(console.error);
