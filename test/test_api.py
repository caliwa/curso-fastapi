import time

from fastapi.testclient import TestClient
import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from main import app
from app.db.models import Base
from app.hashing import Hash
from app.db.database import get_db

db_path = os.path.join(os.path.dirname(__file__),'test.db')
db_uri = "sqlite:///{}".format(db_path)
SQLALCHEMY_DATABASE_URL = db_uri

engine_test = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine_test, autocommit=False, autoflush=False)
Base.metadata.create_all(bind=engine_test)

cliente = TestClient(app)

def insertar_usuario_prueba():
    password_hash = Hash.hash_password('prueba123')
    engine_test.execute(
        f"""
        INSERT INTO usuario (username, password,nombre,apellido,direccion,telefono,correo)
        values
        ('prueba1','{password_hash}','prueba_nombre','prueba_apellido','prueba_direccion',1234,'prueba1@gmail.com')
        """
    )

insertar_usuario_prueba()
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
app.dependency_overrides[get_db] = override_get_db

def test_crear_usuario():
    usuario = {
      "username": "dasda",
      "password": "adasd",
      "nombre": "dasdas",
      "apellido": "sada",
      "direccion": "sdaad",
      "telefono": 3123,
      "correo": "FASD@qdas.es",
      "creacion_user": "2022-10-17T23:11:42.511271"
    }

    response = cliente.post('/user/', json=usuario)
    assert response.status_code == 401

    usuario_login = {
        "username": "prueba1",
        "password": "prueba123"
    }
    response_token = cliente.post('/login/', data=usuario_login)
    assert response_token.status_code == 200
    assert response_token.json()['token_type'] == 'bearer'
    headers = {
        "Authorization": f"Bearer {response_token.json()['access_token']}"
    }
    response = cliente.post('/user/', json=usuario, headers=headers)
    assert response.status_code == 201
    assert response.json()['Response'] == "Usuario creado satisfactoriamente!"
    #print(response.json())
    #print(response, dir(response), "status", response.status_code)
    #print(response.json())
    #assert response.json()["Response"] == "Usuario creado satisfactoriamente!"
def test_obtener_usuarios():
    usuario_login = {
        "username": "prueba1",
        "password": "prueba123"
    }
    response_token = cliente.post('/login/', data=usuario_login)
    assert response_token.status_code == 200
    assert response_token.json()['token_type'] == 'bearer'

    headers = {
        "Authorization": f"Bearer {response_token.json()['access_token']}",
    }
    response = cliente.get('/user/', headers=headers)
    assert len(response.json()) == 2

def test_obtener_usuario():
    response = cliente.get('/user/1')
    assert response.json()['username'] == 'prueba1'
    # print(response.json())

def test_eliminar_usuario():
    response = cliente.delete('/user/1')
    assert response.json()['Response'] == 'Usuario eliminado correctamente'
    response_user = cliente.get('/user/1')
    assert response_user.json()['detail'] == 'No existe el usuario con el id 1'

def test_actualizar_usuario():
    usuario = {
      "username": "prueba1_actualizado"
    }
    response = cliente.patch('/user/2', json=usuario)
    assert response.json()['Response'] == 'Usuario actualizado correctamente'
    response_user = cliente.get('/user/2')
    assert response_user.json()['username'] == 'prueba1_actualizado'
    assert response_user.json()['nombre'] == 'dasdas'
def test_delete_database():
    db_path = os.path.join(os.path.dirname(__file__), 'test.db')
    os.remove(db_path)