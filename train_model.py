import pandas as pd
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
import pickle

# Cargar datos
df_ratings = pd.read_csv("ratings.csv")
df_movies = pd.read_csv("movies.csv")

# Verificar y eliminar datos faltantes en ratings
print("Datos faltantes en ratings:")
print(df_ratings.isnull().sum())
df_ratings = df_ratings.dropna()  # Eliminar filas con datos faltantes

# Verificar y eliminar datos faltantes en movies
print("\nDatos faltantes en movies:")
print(df_movies.isnull().sum())
df_movies = df_movies.dropna()  # Eliminar filas con datos faltantes

# Eliminar duplicados en ratings
print("\nRatings duplicados:", df_ratings.duplicated().sum())
df_ratings = df_ratings.drop_duplicates()

# Verificar valores fuera de rango en ratings
print("\nRatings fuera de rango:")
invalid_ratings = df_ratings[~df_ratings["rating"].isin([x/2 for x in range(1, 11)])]
print(invalid_ratings)

# Eliminar valores fuera de rango en ratings
df_ratings = df_ratings[df_ratings["rating"].isin([x/2 for x in range(1, 11)])]

# Verificar usuarios con menos de 5 ratings
user_counts = df_ratings["userId"].value_counts()
print("\nUsuarios con menos de 5 ratings:")
print(user_counts[user_counts < 5])

# Eliminar usuarios con menos de 5 ratings
df_ratings = df_ratings[df_ratings["userId"].isin(user_counts[user_counts >= 5].index)]

# Verificar películas con menos de 5 ratings
movie_counts = df_ratings["movieId"].value_counts()
print("\nPelículas con menos de 5 ratings:")
print(movie_counts[movie_counts < 5])

# Eliminar películas con menos de 5 ratings
df_ratings = df_ratings[df_ratings["movieId"].isin(movie_counts[movie_counts >= 5].index)]

# Crear el dataset de Surprise
reader = Reader(rating_scale=(0.5, 5.0))
data = Dataset.load_from_df(df_ratings[['userId', 'movieId', 'rating']], reader)

# Dividir en conjunto de entrenamiento y prueba
trainset, testset = train_test_split(data, test_size=0.2)

# Entrenar el modelo SVD
model = SVD(n_factors=50, n_epochs=20, random_state=42)
model.fit(trainset)

# Guardar el modelo entrenado
with open("model/modelo_svd.pkl", "wb") as f:
    pickle.dump(model, f)

print("Modelo entrenado y guardado exitosamente.")

from surprise import accuracy

# Predecir en el conjunto de prueba
predictions = model.test(testset)

# Calcular métricas
rmse = accuracy.rmse(predictions)
mae = accuracy.mae(predictions)

print(f"RMSE: {rmse}")
print(f"MAE: {mae}")
