import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg
import jwt
from kafka import KafkaProducer
from datetime import datetime
from functools import wraps

app = Flask(__name__)
# Enable CORS for frontend connectivity
CORS(app)

DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = os.environ.get('DB_PORT', '5432')
DB_NAME = os.environ.get('DB_NAME', 'gimnasio_norte')
DB_USER = os.environ.get('DB_USER', 'user')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'password')
KAFKA_BROKER = os.environ.get('KAFKA_BROKER', 'localhost:9092')

try:
    producer = KafkaProducer(
        bootstrap_servers=[KAFKA_BROKER],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
except Exception as e:
    print(f"Error connecting to Kafka: {e}")
    producer = None

def get_db_connection():
    return psycopg.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME,
        user=DB_USER, password=DB_PASSWORD
    )

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Athlete (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(255) NOT NULL,
            last_name VARCHAR(255) NOT NULL,
            weight FLOAT,
            height FLOAT
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Routine (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            difficulty VARCHAR(50)
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS AthleteRoutine (
            id SERIAL PRIMARY KEY,
            athlete_id INT REFERENCES Athlete(id),
            routine_id INT REFERENCES Routine(id),
            assigned_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'message': 'Token is missing!'}), 401
        token = auth_header.split(" ")[1] if len(auth_header.split(" ")) > 1 else auth_header
        try:
            data = jwt.decode(token, options={"verify_signature": False})
        except Exception as e:
            return jsonify({'message': 'Token is invalid!'}), 403
        return f(*args, **kwargs)
    return decorated

@app.route('/api/athletes', methods=['GET'])
@token_required
def get_athletes():
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('SELECT * FROM Athlete')
        rows = cur.fetchall()
        athletes = [{'id': r[0], 'first_name': r[1], 'last_name': r[2], 'weight': r[3], 'height': r[4]} for r in rows]
        return jsonify(athletes), 200
    finally:
        cur.close()
        conn.close()

@app.route('/api/athletes', methods=['POST'])
@token_required
def create_athlete():
    data = request.json
    if not data or 'first_name' not in data or 'last_name' not in data:
        return jsonify({'error': 'first_name and last_name are required'}), 400
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO Athlete (first_name, last_name, weight, height) VALUES (%s, %s, %s, %s) RETURNING id',
            (data['first_name'], data['last_name'], data.get('weight'), data.get('height'))
        )
        athlete_id = cur.fetchone()[0]
        conn.commit()
        
        if producer:
            producer.send('auditoria.gyms', {
                'tenant': 'Gimnasio Norte',
                'action': 'CREATE_ATHLETE',
                'athlete_id': athlete_id,
                'timestamp': datetime.utcnow().isoformat()
            })
            producer.flush()
        return jsonify({'message': 'Athlete created successfully', 'id': athlete_id}), 201
    except Exception as e:
        if 'conn' in locals(): conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        if 'cur' in locals(): cur.close()
        if 'conn' in locals(): conn.close()

@app.route('/api/routines', methods=['GET'])
@token_required
def get_routines():
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('SELECT * FROM Routine')
        rows = cur.fetchall()
        routines = [{'id': r[0], 'name': r[1], 'description': r[2], 'difficulty': r[3]} for r in rows]
        return jsonify(routines), 200
    finally:
        cur.close()
        conn.close()

@app.route('/api/routines', methods=['POST'])
@token_required
def create_routine():
    data = request.json
    if not data or 'name' not in data:
        return jsonify({'error': 'name is required'}), 400
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('INSERT INTO Routine (name, description, difficulty) VALUES (%s, %s, %s) RETURNING id',
                    (data['name'], data.get('description'), data.get('difficulty')))
        routine_id = cur.fetchone()[0]
        conn.commit()
        return jsonify({'message': 'Routine created successfully', 'id': routine_id}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

@app.route('/api/athletes/<int:athlete_id>/routines', methods=['POST'])
@token_required
def assign_routine(athlete_id):
    data = request.json
    if not data or 'routine_id' not in data:
        return jsonify({'error': 'routine_id is required'}), 400
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('INSERT INTO AthleteRoutine (athlete_id, routine_id) VALUES (%s, %s) RETURNING id',
                    (athlete_id, data['routine_id']))
        assignment_id = cur.fetchone()[0]
        conn.commit()
        if producer:
            producer.send('auditoria.gyms', {
                'tenant': 'Gimnasio Norte',
                'action': 'ROUTINE_ASSIGNED',
                'athlete_id': athlete_id,
                'routine_id': data['routine_id'],
                'timestamp': datetime.utcnow().isoformat()
            })
            producer.flush()
        return jsonify({'message': 'Routine assigned successfully', 'id': assignment_id}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    try:
        init_db()
    except Exception as e:
        print(f"Could not initialize DB: {e}")
    app.run(host='0.0.0.0', port=5000)
