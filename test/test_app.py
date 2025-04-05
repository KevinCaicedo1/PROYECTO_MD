# tests/test_app.py
import pytest
import json
import sys
import os
from app import app
from confluent_kafka import Producer 
 # Ahora Python puede encontrar app.py 

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_recommendations(client):
    # Realiza una solicitud GET al endpoint de recomendaciones para un usuario
    response = client.get("/recommend/1")
    
    # Verificar que la respuesta tiene código de estado 200
    assert response.status_code == 200
    
    # Verificar que la respuesta contiene una lista de recomendaciones
    recomendaciones = response.data.decode("utf-8")
    assert len(recomendaciones.split(",")) > 0  # Debe haber al menos una recomendación



