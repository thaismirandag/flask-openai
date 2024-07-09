import logging
from flask import Blueprint, jsonify, request
from openai import AuthenticationError, OpenAIError
from .services import AssistantPetLoveService

api_openai = Blueprint('api', __name__, url_prefix='/api/ecommerce/v1')

service = AssistantPetLoveService()

@api_openai.route('/question-and-answer', methods=['POST'])
def ask_question():
    try:
        data = request.get_json()
        if not data or "question" not in data:
            return jsonify({"error": "Dados não fornecidos"}), 400

        question = data.get("question", "").strip()

        if not question:
            return jsonify({"error": "Pergunta não pode ser vazia"}), 400

        response = service.get_response(question)
        formatted_response = service.format_response(response)
        return jsonify({"response":formatted_response}), 200

    except AuthenticationError as e:
        logging.error("Erro de autenticação: %s", e)
        return jsonify({"error": "Chave da API OpenAI incorreta"}), 401
    except OpenAIError as e:
        logging.error("Erro ao obter resposta: %s", e)
        return jsonify({"error": "Erro para obter alguma resposta da API"}), 500
    except Exception as e:
        logging.error("Erro inesperado ao obter resposta: %s", e)
        return jsonify({"error": "Ocorreu um erro para obter uma resposta"}), 500