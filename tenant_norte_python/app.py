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

import time

producer = None
for attempt in range(15):
    try:
        producer = KafkaProducer(
            bootstrap_servers=[KAFKA_BROKER],
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        print("Connected to Kafka successfully")
        break
    except Exception as e:
        print(f"Error connecting to Kafka (attempt {attempt+1}/15): {e}")
        time.sleep(3)

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
            height FLOAT,
            keycloak_username VARCHAR(255)
        )
    ''')
    cur.execute('ALTER TABLE Athlete ADD COLUMN IF NOT EXISTS keycloak_username VARCHAR(255);')
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
        if request.method == 'OPTIONS':
            return jsonify({'message': 'OK'}), 200
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

@app.route('/api/athletes', methods=['GET', 'OPTIONS'])
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

@app.route('/api/audit/login', methods=['POST', 'OPTIONS'])
@token_required
def audit_login():
    """
    Endpoint de auditoría que registra en Kafka los inicios de sesión exitosos.
    El nombre de usuario se extrae del JWT validado.
    """
    auth_header = request.headers.get('Authorization')
    token = auth_header.split(" ")[1] if len(auth_header.split(" ")) > 1 else auth_header
    data = jwt.decode(token, options={"verify_signature": False})
    
    username = data.get('preferred_username', 'Unknown')
    if producer:
        try:
            producer.send('auditoria.gyms', {
                'action': 'USER_LOGIN',
                'tenant': 'Gimnasio Norte',
                'user': username,
                'timestamp': datetime.now().isoformat()
            })
            producer.flush()
        except Exception as kafka_err:
            print(f"Error sending login audit to Kafka: {kafka_err}")
    return jsonify({'status': 'logged'}), 200

@app.route('/api/athletes', methods=['POST', 'OPTIONS'])
@token_required
def create_athlete():
    """
    Crea un nuevo expediente físico de atleta en la base de datos PostgreSQL.
    Registra el evento de creación en Kafka para el control de auditoría global.
    """
    data = request.json
    if not data or 'first_name' not in data or 'last_name' not in data:
        return jsonify({'error': 'first_name and last_name are required'}), 400
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO Athlete (first_name, last_name, weight, height, keycloak_username) VALUES (%s, %s, %s, %s, %s) RETURNING id',
            (data['first_name'], data['last_name'], data.get('weight'), data.get('height'), data.get('keycloak_username'))
        )
        athlete_id = cur.fetchone()[0]
        conn.commit()
        
        if producer:
            try:
                producer.send('auditoria.gyms', {
                    'tenant': 'Gimnasio Norte',
                    'action': 'CREATE_ATHLETE',
                    'athlete_id': athlete_id,
                    'timestamp': datetime.utcnow().isoformat()
                })
                producer.flush()
            except Exception as kafka_err:
                print(f"Error sending CREATE_ATHLETE audit to Kafka: {kafka_err}")
        return jsonify({'message': 'Athlete created successfully', 'id': athlete_id}), 201
    except Exception as e:
        if 'conn' in locals(): conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        if 'cur' in locals(): cur.close()
        if 'conn' in locals(): conn.close()

@app.route('/api/athletes/<int:athlete_id>', methods=['DELETE', 'OPTIONS'])
@token_required
def delete_athlete(athlete_id):
    """
    Elimina físicamente el registro de un atleta y todas sus asignaciones asociadas.
    Emite un evento de eliminación a Kafka para mantener la trazabilidad de los datos.
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('DELETE FROM AthleteRoutine WHERE athlete_id = %s', (athlete_id,))
        cur.execute('DELETE FROM Athlete WHERE id = %s', (athlete_id,))
        conn.commit()

        if producer:
            try:
                producer.send('auditoria.gyms', {
                    'tenant': 'Gimnasio Norte',
                    'action': 'DELETE_ATHLETE',
                    'athlete_id': athlete_id,
                    'timestamp': datetime.now().isoformat()
                })
                producer.flush()
            except Exception as kafka_err:
                print(f"Error sending DELETE_ATHLETE audit to Kafka: {kafka_err}")

        return jsonify({'message': 'Athlete deleted successfully'}), 200
    except Exception as e:
        if 'conn' in locals(): conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        if 'cur' in locals(): cur.close()
        if 'conn' in locals(): conn.close()

@app.route('/api/routines', methods=['GET', 'OPTIONS'])
@token_required
def get_routines():
    """
    Devuelve el catálogo global de rutinas disponibles en el tenant actual.
    Utilizado por ambos roles (Administrador y Cliente) para consultar la oferta deportiva.
    """
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

@app.route('/api/routines', methods=['POST', 'OPTIONS'])
@token_required
def create_routine():
    """
    Añade una nueva rutina al catálogo global y reporta la creación a Kafka.
    """
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

        if producer:
            try:
                producer.send('auditoria.gyms', {
                    'tenant': 'Gimnasio Norte',
                    'action': 'CREATE_ROUTINE',
                    'routine_name': data['name'],
                    'timestamp': datetime.now().isoformat()
                })
                producer.flush()
            except Exception as kafka_err:
                print(f"Error sending CREATE_ROUTINE audit to Kafka: {kafka_err}")

        return jsonify({'message': 'Routine created successfully', 'id': routine_id}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

@app.route('/api/routines/<int:routine_id>', methods=['DELETE', 'OPTIONS'])
@token_required
def delete_routine(routine_id):
    """
    Elimina una rutina del catálogo. Incluye borrado en cascada manual de las asignaciones existentes.
    Reporta la eliminación al broker de Kafka.
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('DELETE FROM AthleteRoutine WHERE routine_id = %s', (routine_id,))
        cur.execute('DELETE FROM Routine WHERE id = %s', (routine_id,))
        conn.commit()

        if producer:
            try:
                producer.send('auditoria.gyms', {
                    'tenant': 'Gimnasio Norte',
                    'action': 'DELETE_ROUTINE',
                    'routine_id': routine_id,
                    'timestamp': datetime.now().isoformat()
                })
                producer.flush()
            except Exception as kafka_err:
                print(f"Error sending DELETE_ROUTINE audit to Kafka: {kafka_err}")

        return jsonify({'message': 'Routine deleted successfully'}), 200
    except Exception as e:
        if 'conn' in locals(): conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        if 'cur' in locals(): cur.close()
        if 'conn' in locals(): conn.close()

@app.route('/api/audit/training', methods=['POST', 'OPTIONS'])
@token_required
def audit_training():
    """
    Registra en el log de auditoría (Kafka) cuando un atleta inicia un entrenamiento.
    Extrae la rutina del cuerpo de la petición y el usuario del token JWT.
    """
    req_data = request.json
    routine_name = req_data.get('routine_name', 'Unknown Routine') if req_data else 'Unknown Routine'
    
    auth_header = request.headers.get('Authorization')
    token = auth_header.split(" ")[1] if len(auth_header.split(" ")) > 1 else auth_header
    jwt_data = jwt.decode(token, options={"verify_signature": False})
    username = jwt_data.get('preferred_username', 'Unknown')
    
    if producer:
        try:
            producer.send('auditoria.gyms', {
                'action': 'TRAINING_STARTED',
                'tenant': 'Gimnasio Norte',
                'user': username,
                'routine': routine_name,
                'timestamp': datetime.now().isoformat()
            })
            producer.flush()
        except Exception as kafka_err:
            print(f"Error sending TRAINING_STARTED audit to Kafka: {kafka_err}")
    return jsonify({'status': 'training_logged'}), 200
if __name__ == '__main__':
    db_initialized = False
    for attempt in range(15):
        try:
            init_db()
            print("Database initialized successfully")
            db_initialized = True
            break
        except Exception as e:
            print(f"Could not initialize DB (attempt {attempt+1}/15): {e}")
            time.sleep(3)
            
    if not db_initialized:
        print("Failed to initialize database. Exiting...")
        import sys
        sys.exit(1)
        
    app.run(host='0.0.0.0', port=5000)
