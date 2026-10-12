import pytest
from fastapi.testclient import TestClient

from app.main import app, reset_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def limpa_banco():
    reset_db()
    yield
    reset_db()


def test_lista_comeca_vazia():
    resposta = client.get("/tasks")
    assert resposta.status_code == 200
    assert resposta.json() == []


def test_cria_tarefa():
    resposta = client.post("/tasks", json={"title": "Estudar Git"})
    assert resposta.status_code == 201
    assert resposta.json() == {"id": 1, "title": "Estudar Git", "done": False}


def test_atualiza_tarefa_inexistente_retorna_404():
    resposta = client.put("/tasks/99", json={"title": "Fantasma", "done": True})
    assert resposta.status_code == 404
