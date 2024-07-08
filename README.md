# Projeto API Flask com Integração OpenAI

Este projeto consiste em uma API desenvolvida com Flask que integra o serviço OpenAI. A aplicação é containerizada utilizando docker.

## Pré-requisitos

- Docker
- Docker Compose
- Python 3.8 ou acima
- Conta e chave API do OpenAI

## Configuração do Ambiente

### Variável de ambiente

Crie um arquivo .env na raiz do projeto e defina a chave da API do OpenAI:
```
OPENAI_API_KEY= "<KEY>"
```
### Docker

Para iniciar a aplicação usando docker, execute os seguintes comandos:
```sh
docker-compose build
# para o build da imagem

docker-compose up
# para inicializar o container
```
A aplicação vai estar disponível em http://localhost:3000.

