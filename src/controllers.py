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
            logging.warning("Dados não fornecidos")
            return jsonify({"error": "Dados não fornecidos"}), 400
        
        question = data.get("question", "").strip()

        if not question:
            logging.warning("Pergunta não pode ser vazia")
            return jsonify({"error": "Pergunta não pode ser vazia"}), 400
        
        response = service.get_response(question)
        return jsonify({"response": response}), 200

    except AuthenticationError as auth_error:
        logging.error("Erro de autenticação: %s", auth_error)
        return jsonify({"error": "Erro de autenticação"}), 401
    
    except OpenAIError as openai_error:
        logging.error("Erro do OpenAI: %s", openai_error)
        return jsonify({"error": "Erro ao processar a solicitação com o OpenAI"}), 500
    
    except Exception as exception:
        logging.error("Erro inesperado: %s", exception)
        return jsonify({"error": "Erro inesperado para obter uma resposta"}), 500

