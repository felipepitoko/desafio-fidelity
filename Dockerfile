# Use uma imagem base oficial do Python. A versão 'slim' é menor.
FROM python:3.11-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Instala dependências do sistema operacional necessárias para o Selenium e Chrome
# O `wget` e `unzip` são usados para baixar e extrair o chromedriver
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    --no-install-recommends

# Adiciona o repositório do Google Chrome e instala a versão estável
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    --no-install-recommends

# Copia o arquivo de dependências do Python primeiro para aproveitar o cache do Docker
COPY requirements.txt .

# Instala as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o resto do código da aplicação para o diretório de trabalho
COPY . .

# Define o comando padrão para executar quando o contêiner iniciar
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]