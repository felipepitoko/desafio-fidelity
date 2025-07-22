# Robô de Enriquecimento de Pesquisas

![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100-green.svg)
![Docker](https://img.shields.io/badge/Docker-24.0-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

Uma aplicação robusta para fazer o controle de pesquisas, automatizando o enriquecimento desses dados sob demanda. Construída com uma arquitetura de microsserviços usando FastAPI, Selenium e PostgreSQL.

---

## 🚀 Funcionalidades Principais

*   **API RESTful**: Interface baseada em FastAPI para gerenciar e consultar o status das pesquisas.
*   **Worker Assíncrono**: Um serviço de background que busca e processa tarefas de forma contínua e independente da API.
*   **Processamento Paralelo**: Utiliza multithreading para executar múltiplas tarefas de web scraping simultaneamente, aumentando a performance.
*   **Persistência de Dados**: Armazena todas as tarefas, tipos de busca e logs em um banco de dados PostgreSQL.
*   **Containerização Completa**: Toda a aplicação (API, Worker, Banco de Dados) é orquestrada com Docker e Docker Compose para um setup rápido e consistente.
*   **Logging Estruturado**: Gera arquivos de log (`api.log`, `worker.log`) para fácil monitoramento e depuração.

## 🏛️ Arquitetura

O sistema é dividido em serviços independentes que se comunicam entre si:

*   **`API` (FastAPI)**: O ponto de entrada. Expõe endpoints para criar novas pesquisas, consultar tarefas pendentes/concluídas e registrar resultados.
*   **`Worker` (Python/Selenium)**: O "cérebro" da operação. Roda em um loop infinito, consulta a API para obter tarefas pendentes, instancia o `Scraper` para executá-las e envia os resultados de volta para a API.
*   **`Database` (PostgreSQL)**: O "coração" do sistema. Armazena todas as informações de forma persistente.
*   **`Adminer`**: Uma ferramenta leve de gerenciamento de banco de dados para fácil visualização e depuração dos dados.

## ⚙️ Como Executar (Docker)

A maneira mais simples e recomendada de rodar a aplicação é usando Docker.

### Pré-requisitos

*   Docker
*   Docker Compose

### Passos

1.  **Clone o repositório:**
    ```bash
    git clone <url-do-seu-repositorio>
    cd desafio-fidelity
    ```

2.  **Configure o ambiente:**
    Copie o arquivo de exemplo `.env.example` para um novo arquivo chamado `.env` e preencha com suas credenciais.
    ```bash
    cp .env.example .env
    ```
    *Edite o arquivo `.env` com os dados do seu banco de dados.*

3.  **Construa e inicie os contêineres:**
    Este comando irá construir a imagem da aplicação, baixar as imagens do PostgreSQL e Adminer, e iniciar todos os serviços.
    ```bash
    docker-compose up --build
    ```

4.  **Inicialize o banco de dados:**
    Em um **novo terminal**, execute o script de inicialização para criar as tabelas e popular com dados de exemplo.
    ```bash
    docker-compose exec api python db_startup.py
    ```

5.  **Acesse os serviços:**
    *   **Documentação da API (Swagger)**: http://localhost:8000/docs
    *   **Adminer (Gerenciador do Banco)**: http://localhost:8080
        *   **Sistema**: `PostgreSQL`
        *   **Servidor**: `db`
        *   **Usuário/Senha/Banco**: Use os valores do seu arquivo `.env`.

## 💻 Rodando Localmente (Sem Docker)

1.  **Instale e configure o PostgreSQL** na sua máquina.
2.  **Crie um ambiente virtual** e instale as dependências:
    ```bash
    python -m venv venv
    source venv/bin/activate  # ou venv\Scripts\activate no Windows
    pip install -r requirements.txt
    ```
3.  **Configure o arquivo `.env`** para apontar para seu banco de dados local (`DB_HOST=localhost`).
4.  **Inicialize o banco de dados**:
    ```bash
    python db_startup.py
    ```
5.  **Inicie a API** em um terminal:
    ```bash
    uvicorn api:app --reload
    ```
6.  **Inicie o Worker** em outro terminal:
    ```bash
    python worker.py
    ```

## 📝 Endpoints da API

A documentação completa e interativa está disponível em `/docs`.

*   `POST /pesquisas/`: Cria uma nova tarefa de pesquisa.
*   `GET /pesquisas/pendentes/{id}`: Lista tarefas pendentes para um tipo de enriquecimento.
*   `GET /pesquisas/concluidas/`: Lista pesquisas já concluídas.
*   `GET /tipos-enriquecimento/`: Lista todos os tipos de busca disponíveis.
*   `POST /logs/`: Endpoint interno para o Worker registrar os resultados.
*   `GET /health-check/`: Verifica a saúde da API.

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.
