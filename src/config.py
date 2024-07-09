import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        load_dotenv()
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.__validate_openai_api_key()

    def __validate_openai_api_key(self):
        if self.openai_api_key is None:
            raise ValueError("Chave da API OpenAI não encontrada.")
