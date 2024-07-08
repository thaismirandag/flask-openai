from flask import Flask
from src.controllers import api_openai

app = Flask(__name__)

@app.route('/')
def home():
    return "Assistente de vendas da PetLove"

app.register_blueprint(api_openai)
