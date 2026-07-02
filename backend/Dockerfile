FROM python:3.12-slim

WORKDIR /app

# Dependências de sistema mínimas (build de libs como uvicorn[standard])
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

EXPOSE 8000

# --reload funciona pq vamos montar ./backend/app como volume no compose
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
