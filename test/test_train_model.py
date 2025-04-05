# tests/test_train_model.py
import os
import pytest
import pickle
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
from surprise import accuracy
import pandas as pd

def test_model_training():
    # Cargar datos
    df_ratings = pd.read_csv("ratings.csv")
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

    # Asegurar que el modelo se guarda correctamente
    assert os.path.exists("model/modelo_svd.pkl") == True

    # Predecir en el conjunto de prueba
    predictions = model.test(testset)

    # Calcular métricas
    rmse = accuracy.rmse(predictions)
    mae = accuracy.mae(predictions)

    # Asegurar que las métricas son razonables
    assert rmse < 1.0  # Un valor RMSE bajo
    assert mae < 1.0   # Un valor MAE bajo
