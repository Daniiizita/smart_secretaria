# Estágio 1: Base
# Usamos uma imagem Python oficial e slim para manter o tamanho reduzido.
FROM python:3.11-slim-buster

# Define variáveis de ambiente para boas práticas em containers Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Instala dependências do sistema, se necessário.
# No nosso caso, não há, mas é bom saber onde colocar.
# RUN apt-get update && apt-get install -y ...

# Copia o arquivo de dependências primeiro para aproveitar o cache do Docker.
# O Docker só irá reinstalar as dependências se este arquivo mudar.
COPY requirements.txt .

# Instala as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da aplicação para o diretório de trabalho
COPY . .

# Expõe a porta que o Django runserver usará
EXPOSE 8000
