import logging
from flask import Flask
from src.controllers import api_openai


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


app = Flask(__name__)

@app.route('/')
def home():
    return "Assistente de vendas da PetLove"

app.register_blueprint(api_openai)
