from flask import Flask, jsonify, request
import pickle
import pandas as pd
from surprise import Dataset, Reader
import time
from confluent_kafka import Producer
from multiprocessing import Process
import monitoring.logger as logger

app = Flask(__name__)
app.config['TESTING'] = True  # Habilita el modo de pruebas
app.config['DEBUG'] = False 
# Configurar el Productor de Kafka
KAFKA_TOPIC = "recommendationsNew"
KAFKA_BROKER = "localhost:9092"  # Cambiar si Kafka está en otro host
producer = Producer({'bootstrap.servers': KAFKA_BROKER})

# Cargar el modelo previamente entrenado
with open("model/modelo_svd.pkl", "rb") as f:
    model = pickle.load(f)

# Cargar el dataset para obtener IDs de películas
df_movies = pd.read_csv("movies.csv")
df_ratings = pd.read_csv("ratings.csv")

def obtener_recomendaciones(user_id, model, df_movies, df_ratings, n=20):
    all_movie_ids = set(df_movies["movieId"].unique())
    rated_movies = set(df_ratings[df_ratings["userId"] == user_id]["movieId"].unique())
    unseen_movies = list(all_movie_ids - rated_movies)
    
    predictions = [model.predict(user_id, movie_id) for movie_id in unseen_movies]
    predictions.sort(key=lambda x: x.est, reverse=True)  
    return [int(pred.iid) for pred in predictions[:n]]

@app.route("/recommend/<int:user_id>", methods=["GET"])
def recomendar(user_id):
    start_time = time.time()  # Medir tiempo de respuesta
    try:
        recomendaciones = obtener_recomendaciones(user_id, model, df_movies, df_ratings)
        response_time = round((time.time() - start_time) * 1000, 2)  # Milisegundos
        # recomendaciones sin comas solo separadas por espacios
        recomendacionesKafka = " ".join(map(str, recomendaciones))
        # Formato del mensaje para Kafka
        kafka_message = f"{time.time()},{user_id},recommendation request {request.host}, status 200, result: {recomendacionesKafka},{response_time} ms"
        
        # Enviar mensaje a Kafka
        producer.produce(KAFKA_TOPIC, key=str(user_id), value=kafka_message)
        producer.flush()  # Asegurar envío
        
        return ",".join(map(str, recomendaciones)), 200
    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    # Lanzar el logger como proceso paralelo
    #p = Process(target=logger.iniciar_logger)
    #p.start()
    app.run(host="0.0.0.0", port=8082)
