from unittest.mock import patch, Mock
import pytest
from src.services import AssistantPetLoveService
from src.prompts import petlove_assistant_prompt

class MockConfig:
    openai_api_key = "api_openai_fake_key"

@pytest.fixture
def reset_key_mock():
    api_key = MockConfig.openai_api_key
    yield
    MockConfig.openai_api_key = api_key

class TestAssistantPetLoveService:

    @patch('src.services.Config', new=MockConfig)
    @patch('src.services.OpenAI')
    @patch('src.services.LLMChain')
    def test_initialization_sucess(self, mock_llm_chain, mock_openai, reset_key_mock):
        service = AssistantPetLoveService()
        assert service.api_key == "api_openai_fake_key"

        mock_openai_instance = mock_openai.return_value
        mock_openai.assert_called_once_with(model='gpt-3.5-turbo-instruct',
                                            temperature=0,
                                            max_tokens=500,
                                            api_key='api_openai_fake_key')
        mock_llm_chain.return_value = Mock()
        mock_llm_chain.assert_called_once_with(llm=mock_openai_instance,
                                               prompt=petlove_assistant_prompt)
   
        assert service.llm is not None
        assert service.llm_chain is not None

    @patch('src.services.Config', new=MockConfig)
    def test_initialization_failure(self, reset_key_mock):
        MockConfig.openai_api_key = None
        with pytest.raises(ValueError, match="Chave da API da OpenAI não encontrada!"):
            AssistantPetLoveService()

    @patch('src.services.Config', new=MockConfig)
    @patch('src.services.OpenAI')
    @patch('src.services.LLMChain')
    def test_get_response_function_success(self, mock_llm_chain, reset_key_mock):
        mock_llm_chain_instance = mock_llm_chain.return_value
        mock_llm_chain_instance.invoke.return_value = {"text": "Resposta teste"}

        service = AssistantPetLoveService()
        question = "Qual a melhor ração para golden?"
        response = service.get_response(question)
        assert response == "Resposta teste"

        mock_llm_chain_instance.invoke.assert_called_once_with({"question":
                                                                "Qual a melhor ração para golden?"})

    @patch('src.services.Config', new=MockConfig)
    @patch('src.services.OpenAI')
    @patch('src.services.LLMChain')
    def test_get_response_function_failure(self, mock_llm_chain, reset_key):
        mock_llm_chain_instance = mock_llm_chain.return_value
        mock_llm_chain_instance.invoke.side_effect = Exception("Simulação de erro")

        service = AssistantPetLoveService()
        question = "Qual a melhor ração para golden?"
        response = service.get_response(question)

        assert response == {"error": "Erro inesperado para obter uma resposta"}
        mock_llm_chain_instance.invoke.assert_called_once_with({"question":
                                                                "Qual a melhor ração para golden?"})
