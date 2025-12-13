FROM python:3.11-slim

# Evita buffer nei log
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Installa dipendenze di sistema necessarie per lxml/bs4
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Dipendenze Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Codice applicativo
COPY . .

# Avvia lo scheduler
CMD ["python", "scheduler.py"]
