const express = require('express');
const cors = require('cors');
const mysql = require('mysql2/promise');
const jwt = require('jsonwebtoken');
const { Kafka } = require('kafkajs');

const app = express();
app.use(cors());
app.use(express.json());

const pool = mysql.createPool({
  host: process.env.DB_HOST || 'localhost',
  user: process.env.DB_USER || 'root',
  password: process.env.DB_PASSWORD || 'rootpassword',
  database: process.env.DB_NAME || 'gimnasio_sur',
  port: process.env.DB_PORT || 3307,
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0
});

const kafka = new Kafka({
  clientId: 'tenant-sur-app',
  brokers: [process.env.KAFKA_BROKER || 'localhost:9092']
});
const producer = kafka.producer();

const initKafka = async () => {
  try {
    await producer.connect();
    console.log('Connected to Kafka successfully');
  } catch (error) {
    console.error('Error connecting to Kafka', error);
  }
};
initKafka();

const authenticateToken = (req, res, next) => {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];
  if (!token) return res.sendStatus(401);

  try {
    const decoded = jwt.decode(token);
    if (!decoded) throw new Error('Invalid token');
    req.user = decoded;
    next();
  } catch (err) {
    return res.status(403).json({ message: "Forbidden: Invalid token" });
  }
};

const initDb = async () => {
  await pool.query(`
    CREATE TABLE IF NOT EXISTS Athlete (
      id INT AUTO_INCREMENT PRIMARY KEY,
      first_name VARCHAR(255) NOT NULL,
      last_name VARCHAR(255) NOT NULL,
      weight FLOAT,
      height FLOAT
    )
  `);
  await pool.query(`
    CREATE TABLE IF NOT EXISTS Routine (
      id INT AUTO_INCREMENT PRIMARY KEY,
      name VARCHAR(255) NOT NULL,
      description TEXT,
      difficulty VARCHAR(50)
    )
  `);
  await pool.query(`
    CREATE TABLE IF NOT EXISTS AthleteRoutine (
      id INT AUTO_INCREMENT PRIMARY KEY,
      athlete_id INT,
      routine_id INT,
      assigned_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (athlete_id) REFERENCES Athlete(id),
      FOREIGN KEY (routine_id) REFERENCES Routine(id)
    )
  `);
};
initDb().catch(console.error);

// Endpoints Athlete
app.post('/api/athletes', authenticateToken, async (req, res) => {
  const { first_name, last_name, weight, height } = req.body;
  if (!first_name || !last_name) return res.status(400).json({ error: 'first_name and last_name are required' });

  try {
    const [result] = await pool.query(
      'INSERT INTO Athlete (first_name, last_name, weight, height) VALUES (?, ?, ?, ?)',
      [first_name, last_name, weight || null, height || null]
    );
    const athleteId = result.insertId;

    await producer.send({
      topic: 'auditoria.gyms',
      messages: [{ value: JSON.stringify({
        tenant: 'Gimnasio Sur',
        action: 'CREATE_ATHLETE',
        athlete_id: athleteId,
        timestamp: new Date().toISOString()
      })}]
    });

    res.status(201).json({ message: 'Athlete created successfully', id: athleteId });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

app.get('/api/athletes', authenticateToken, async (req, res) => {
  try {
    const [rows] = await pool.query('SELECT * FROM Athlete');
    res.status(200).json(rows);
  } catch (error) {
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

// Endpoints Routine
app.get('/api/routines', authenticateToken, async (req, res) => {
  try {
    const [rows] = await pool.query('SELECT * FROM Routine');
    res.status(200).json(rows);
  } catch (error) {
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

app.post('/api/routines', authenticateToken, async (req, res) => {
  const { name, description, difficulty } = req.body;
  if (!name) return res.status(400).json({ error: 'name is required' });

  try {
    const [result] = await pool.query(
      'INSERT INTO Routine (name, description, difficulty) VALUES (?, ?, ?)',
      [name, description || null, difficulty || null]
    );
    res.status(201).json({ message: 'Routine created successfully', id: result.insertId });
  } catch (error) {
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

app.post('/api/athletes/:id/routines', authenticateToken, async (req, res) => {
  const athleteId = req.params.id;
  const { routine_id } = req.body;
  if (!routine_id) return res.status(400).json({ error: 'routine_id is required' });

  try {
    const [result] = await pool.query(
      'INSERT INTO AthleteRoutine (athlete_id, routine_id) VALUES (?, ?)',
      [athleteId, routine_id]
    );

    await producer.send({
      topic: 'auditoria.gyms',
      messages: [{ value: JSON.stringify({
        tenant: 'Gimnasio Sur',
        action: 'ROUTINE_ASSIGNED',
        athlete_id: athleteId,
        routine_id: routine_id,
        timestamp: new Date().toISOString()
      })}]
    });

    res.status(201).json({ message: 'Routine assigned successfully', id: result.insertId });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Node.js backend for Gimnasio Sur running on port ${PORT}`);
});
