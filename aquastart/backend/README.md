# Backend - Generator PDF dla AquaStart

## Instalacja

1. Utwórz plik `.env` na podstawie `.env.example`:
```bash
cp .env.example .env
```

2. Zaktualizuj zmienne środowiskowe w `.env` z twoimi danymi Supabase

3. Zainstaluj zależności Python:
```bash
pip install -r requirements.txt
```

## Użycie

### Generowanie podstawowego PDF
```bash
python pdf_generator.py
```

### Generowanie PDF z niestandardową zawartością
```python
from pdf_generator import generate_aquastart_pdf

content = {
    "pH": 7.0,
    "Temperatura": "25°C",
    "Twardość": "10 dGH"
}

filename, db_response = generate_aquastart_pdf(
    title="AquaStart: Mój Akwarium",
    pdf_type="Raport",
    content=content
)
```

## Struktura

- `pdf_generator.py` - Główny moduł generowania PDF-ów
- `requirements.txt` - Zależności Python
- `.env.example` - Szablon zmiennych środowiskowych

## Wymagania

- Python 3.8+
- Biblioteki wymienione w `requirements.txt`

## Baza danych

Skrypt oczekuje tabeli `pdf_publications` w Supabase z kolumnami:
- `id` (UUID, primary key)
- `title` (text)
- `type` (text)
- `file_url` (text)
- `created_at` (timestamp)
