from unittest.mock import patch, MagicMock
from openai import AuthenticationError, OpenAIError
import pytest
from flask import Flask
from src.controllers import api_openai
from src.services import AssistantPetLoveService

@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(api_openai)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

class ResponseMock:
    def __init__(self, status_code=401):
        self.request = MagicMock()
        self.status_code = status_code
        self.headers = {"X-request-id": "request-id"}

@patch.object(AssistantPetLoveService, 'get_response', return_value="Resposta teste")
def test_ask_question_success(mock_get_response, client):
    response = client.post('/api/ecommerce/v1/question-and-answer',
                           json={"question": "Qual a melhor ração para golden?"})
    assert response.status_code == 200
    assert response.json == {"response": "Resposta teste"}

def test_ask_question_no_question(client):
    response = client.post('/api/ecommerce/v1/question-and-answer',
                           json={})
    assert response.status_code == 400
    assert response.json == {"error": "Dados não fornecidos"}

def test_ask_question_empty(client):
    response = client.post('/api/ecommerce/v1/question-and-answer',
                           json={"question": ""})
    assert response.status_code == 400
    assert response.json == {"error": "Pergunta não pode ser vazia"}

@patch.object(AssistantPetLoveService, 'get_response', side_effect=AuthenticationError("Erro de autenticação", response=ResponseMock(), body="body"))
def test_ask_question_authentication_error(mock_get_response, client):
    response = client.post('/api/ecommerce/v1/question-and-answer',
                           json={"question": "Qual a melhor ração para golden?"})
    assert response.status_code == 401
    assert response.json == {"error": "Erro de autenticação"}

@patch.object(AssistantPetLoveService, 'get_response', side_effect=OpenAIError("Erro da OpenAI"))
def test_ask_question_openai_error(mock_get_response, client):
    response = client.post('/api/ecommerce/v1/question-and-answer',
                           json={"question": "Qual a melhor ração para golden?"})
    assert response.status_code == 500
    assert response.json == {"error": "Erro ao processar a solicitação com o OpenAI"}

@patch.object(AssistantPetLoveService, 'get_response', side_effect=Exception("Erro inesperado"))
def test_ask_question_unexpected_error(mock_get_response, client):
    response = client.post('/api/ecommerce/v1/question-and-answer',
                           json={"question": "Qual a melhor ração para golden?"})
    assert response.status_code == 500
    assert response.json == {"error": "Erro inesperado para obter uma resposta"}
