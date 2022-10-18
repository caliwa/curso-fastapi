from fastapi.testclient import TestClient
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from main import app

cliente = TestClient(app)

def test_crear_usuario():
    usuario = {
      "username": "jesus",
      "password": "dios",
      "nombre": "string",
      "apellido": "string",
      "direccion": "string",
      "telefono": 0,
      "correo": "qeq@qdas.es",
      "creacion_user": "2022-10-17T23:11:42.511271"
    }
    response = cliente.post('/user/', json=usuario)
    assert response.status_code == 201
    #print(response, dir(response), "status", response.status_code)
    #print(response.json())
    assert response.json()["Response"] == "Usuario creado satisfactoriamente!"