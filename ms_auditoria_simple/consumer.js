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
  let connected = false;
  for (let attempt = 1; attempt <= 15; attempt++) {
    try {
      await consumer.connect();
      console.log('Auditoria consumer connected to Kafka successfully');
      connected = true;
      break;
    } catch (error) {
      console.error(`Error connecting Auditoria consumer to Kafka (attempt ${attempt}/15):`, error.message);
      if (attempt < 15) {
        await new Promise(resolve => setTimeout(resolve, 3000));
      }
    }
  }

  if (!connected) {
    console.error('Auditoria consumer failed to connect to Kafka. Exiting...');
    process.exit(1);
  }

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

run().catch(err => {
  console.error('Fatal error in auditoria consumer:', err);
  process.exit(1);
});
