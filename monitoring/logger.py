from confluent_kafka import Consumer
import csv
import os
from datetime import datetime

# Configuración del consumidor de Kafka
KAFKA_TOPIC = "recommendationsNew"
KAFKA_BROKER = "localhost:9092"
KAFKA_GROUP = "logger_group"

# Configuración del archivo CSV de logs
LOG_FILE = "logs_recommendations.csv"
CSV_HEADERS = ["timestamp", "user_id", "origin", "status", "recommendations", "response_time_ms"]

def parse_message(message):
    """
    Parsea el mensaje Kafka en formato CSV: 
    "timestamp,user_id,recommendation request origin, status 200, result: 1 2 3 4,123.45 ms"
    """
    try:
        parts = message.split(",")
        timestamp = datetime.fromtimestamp(float(parts[0])).strftime("%Y-%m-%d %H:%M:%S")
        user_id = parts[1]
        origin = parts[2].replace("recommendation request", "").strip()
        status = parts[3].split()[-1]
        recommendations = parts[4].replace("result:", "").strip()
        response_time = parts[5].replace("ms", "").strip()

        return [timestamp, user_id, origin, status, recommendations, response_time]
    except Exception as e:
        print(f"Error al parsear mensaje: {e}")
        return None

def iniciar_logger():
    consumer = Consumer({
        'bootstrap.servers': KAFKA_BROKER,
        'group.id': KAFKA_GROUP,
        'auto.offset.reset': 'earliest'
    })

    consumer.subscribe([KAFKA_TOPIC])

    print(f"✅ Logger iniciado y escuchando en el topic '{KAFKA_TOPIC}'...")

    # Verificar si el archivo ya existe
    file_exists = os.path.isfile(LOG_FILE)

    with open(LOG_FILE, mode='a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        if not file_exists:
            writer.writerow(CSV_HEADERS)  # Escribir encabezados si es nuevo

        while True:
            msg = consumer.poll(1.0)  # Esperar 1 segundo
            if msg is None:
                continue
            if msg.error():
                print(f"❌ Error al recibir mensaje: {msg.error()}")
                continue

            message = msg.value().decode('utf-8')
            parsed = parse_message(message)

            if parsed:
                writer.writerow(parsed)
                csvfile.flush()  # Forzar guardado inmediato
                print(f"📥 Log registrado para user_id {parsed[1]}")


