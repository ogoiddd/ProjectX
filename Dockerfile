FROM python:3.11-slim

WORKDIR /app

# Instala dependências primeiro (melhor cache de layers)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código
COPY copybot ./copybot
COPY run.py .

# O estado é persistido aqui — monta um volume para sobreviver a reinícios:
#   docker run -v $(pwd)/data:/app/data ...
ENV STATE_FILE=/app/data/state.json

# As credenciais vêm do ambiente (--env-file .env), nunca da imagem.
CMD ["python", "run.py"]
