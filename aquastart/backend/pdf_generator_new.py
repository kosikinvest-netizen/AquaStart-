# -*- coding: utf-8 -*-
"""AquaStart PDF Generator Module.

Moduł odpowiedzialny za generowanie raportów PDF z wykorzystaniem reportlab
i synchronizacją z bazą danych Supabase.

Requirements:
- reportlab>=4.0.0
- supabase>=2.0.0
- python-dotenv>=1.0.0

Environment variables:
- SUPABASE_URL: URL projektu Supabase
- SUPABASE_KEY: Klucz publiczny Supabase (anon/public key)
"""

import logging
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from supabase import create_client
from supabase.client import Client

# Konfiguracja loggingu
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Załaduj zmienne środowiskowe z .env
load_dotenv()

# Konfiguracja katalogów
BASE_DIR = Path(__file__).parent
FONTS_DIR = BASE_DIR / 'fonts'
OUTPUT_DIR = BASE_DIR / 'output'

# Tworzenie katalogów jeśli nie istnieją
FONTS_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# Konfiguracja Supabase z zmiennych środowiskowych
SUPABASE_URL: Optional[str] = os.getenv('SUPABASE_URL')
SUPABASE_KEY: Optional[str] = os.getenv('SUPABASE_KEY')

if not SUPABASE_URL or not SUPABASE_KEY:
    logger.error(
        'Brakuje zmiennych środowiskowych: SUPABASE_URL i/lub SUPABASE_KEY'
    )
    logger.error('Upewnij się, że plik .env zawiera te zmienne.')
    sys.exit(1)

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    logger.info('Klient Supabase zainicjalizowany.')
except Exception as e:
    logger.error(f'Błąd inicjalizacji klienta Supabase: {e}')
    sys.exit(1)

# URL głównej gałęzi DejaVu Fonts
DEJAVU_FONTS_BASE_URL = (
    'https://raw.githubusercontent.com/dejavu-fonts/dejavu-fonts/master/ttf'
)

FONTS_CONFIG = {
    'DejaVuSans.ttf': f'{DEJAVU_FONTS_BASE_URL}/DejaVuSans.ttf',
    'DejaVuSans-Bold.ttf': f'{DEJAVU_FONTS_BASE_URL}/DejaVuSans-Bold.ttf',
}


def download_fonts() -> bool:
    """Pobiera fonty DejaVu z repozytorium GitHub.

    Funkcja automatycznie pobiera fonty DejaVuSans i DejaVuSans-Bold,
    jeśli nie istnieją lokalnie w katalogu fonts/.

    Returns:
        bool: True jeśli wszystkie fonty zostały pobrane/znalezione,
              False w przypadku błędu.
    """
    for filename, url in FONTS_CONFIG.items():
        font_path = FONTS_DIR / filename
        if font_path.exists():
            logger.info(f'Font {filename} znaleziony lokalnie.')
            continue

        logger.info(f'Pobieranie fontu {filename} z {url}...')
        try:
            urllib.request.urlretrieve(url, font_path)
            logger.info(f'Font {filename} pobrany pomyślnie.')
        except urllib.error.URLError as e:
            logger.error(f'Błąd pobierania {filename}: {e}')
            return False
        except Exception as e:
            logger.error(f'Nieoczekiwany błąd podczas pobierania {filename}: {e}')
            return False

    return True


def register_fonts() -> bool:
    """Rejestruje fonty DejaVu w reportlab.

    Funkcja rejestruje fonty DejaVuSans i DejaVuSans-Bold w pdfmetrics,
    aby mogły być używane w generowanych PDF.

    Returns:
        bool: True jeśli wszystkie fonty zostały zarejestrowane,
              False w przypadku błędu.
    """
    for font_name, filename in [
        ('DejaVuSans', 'DejaVuSans.ttf'),
        ('DejaVuSans-Bold', 'DejaVuSans-Bold.ttf'),
    ]:
        font_path = FONTS_DIR / filename
        if not font_path.exists():
            logger.error(f'Plik fontu {font_path} nie istnieje.')
            return False

        try:
            pdfmetrics.registerFont(TTFont(font_name, str(font_path)))
            logger.info(f'Font {font_name} zarejestrowany.')
        except Exception as e:
            logger.error(f'Błąd rejestracji fontu {font_name}: {e}')
            return False

    return True


def generate_aquastart_pdf() -> bool:
    """Generuje PDF z parametrami wody dla systemu AquaStart.

    Funkcja generuje raport PDF zawierający:
    - Tytuł i nagłówek
    - Polskie znaki diakrytyczne
    - Polską typografię (cudzysłowy, półpauzę, znaki chemii)
    - Zakresy temperatur

    Plik jest generowany z sygnaturą %PDF-1.4 (reportlab).

    Returns:
        bool: True jeśli PDF został wygenerowany i zapisany do Supabase,
              False w przypadku błędu.
    """
    # Pobranie i rejestracja fontów
    if not download_fonts():
        logger.error('Nie udało się pobrać fontów.')
        return False

    if not register_fonts():
        logger.error('Nie udało się zarejestrować fontów.')
        return False

    filename = 'AquaStart_Parametry.pdf'
    file_path = OUTPUT_DIR / filename

    logger.info(f'Generowanie PDF: {file_path}')

    try:
        # Inicjalizacja płótna (reportlab automatycznie dodaje sygnaturę %PDF-1.4)
        c = canvas.Canvas(str(file_path), pagesize=A4)

        # Rysowanie treści
        c.setFont('DejaVuSans-Bold', 22)
        c.drawString(50, 750, 'AquaStart: Parametry Wody')

        c.setFont('DejaVuSans', 12)
        c.drawString(50, 700, 'Polskie znaki: ą ę ł ó ś ź ć ż ń')
        c.drawString(
            50,
            675,
            'Typografia: „Złota zasada akwarysty” – umiar w zarządzaniu.',
        )
        c.drawString(50, 650, 'Związki chemiczne: NH₃, CO₂, NO₂')
        c.drawString(50, 625, 'Temperatura: 24°C–26°C (zakres pracy)')

        c.save()
        logger.info(f'Plik wygenerowany: {file_path}')

    except Exception as e:
        logger.error(f'Błąd podczas generowania PDF: {e}')
        return False

    # Zapis metadanych do bazy Supabase
    try:
        response = supabase.table('pdf_publications').insert({
            'title': 'AquaStart: Parametry Wody',
            'type': 'E-book',
            'file_url': str(file_path),
            'status': 'completed',
        }).execute()

        logger.info(
            f'Rekord dodany do bazy danych: {response.data if response.data else ""}'
        )
        return True

    except Exception as e:
        logger.error(f'Błąd zapisu do bazy danych: {e}')
        return False


if __name__ == '__main__':
    success = generate_aquastart_pdf()
    sys.exit(0 if success else 1)
