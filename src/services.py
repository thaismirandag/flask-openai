import logging
from langchain_openai import OpenAI
from langchain.chains.llm import LLMChain
from .prompts import petlove_assistant_prompt
from .config import Config


class AssistantPetLoveService:
    def __init__(self):
        self.config = Config()
        self.api_key = self.config.openai_api_key

        if not self.api_key:
            raise ValueError("Chave da API da OpenAI não encontrada!")

        self.llm = OpenAI(model='gpt-3.5-turbo-instruct',
                           temperature=0,
                           max_tokens=500,
                           api_key=self.api_key)

        self.llm_chain = LLMChain(llm=self.llm,
                                   prompt=petlove_assistant_prompt)

    def get_response(self, question: str) -> str:
        try:
            response = self.llm_chain.invoke({"question": question})
            return self.format_response(response)
        except Exception as exception:
            logging.error("Erro para obter resposta: %s", exception)
            return {"error": "Erro inesperado para obter uma resposta"}

    def format_response(self, data: dict) -> str:
        answer = data.get("text", "Resposta não encontrada")
        return f"{answer}"
