FROM python:3.12-slim

WORKDIR /app/backend

# Zainstaluj zależności systemowe
RUN apt-get update && apt-get install -y \
    fonts-dejavu \
    && rm -rf /var/lib/apt/lists/*

# Skopiuj requirements
COPY requirements.txt .

# Zainstaluj Python zależności
RUN pip install --no-cache-dir -r requirements.txt

# Skopiuj kod
COPY . .

# Uruchom generator
CMD ["python3", "pdf_generator.py"]
