#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AquaStart PDF Generator - Production.

Moduł generdu raportów PDF dla systemu zarządzania akwariami High-Tech.
Integracja z bazą danych Supabase i obsługa fontów DejaVu.

Wymagania:
    - reportlab>=4.0.9
    - supabase>=2.0.4
    - python-dotenv>=1.0.0

Zmienne środowiskowe (.env):
    SUPABASE_URL (str): URL projektu Supabase
    SUPABASE_KEY (str): Klucz publiczny Supabase (anon/public)
    
Użycie:
    python3 pdf_generator.py
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

__version__ = '1.0.0'
__author__ = 'AquaStart'

# ============================================================================
# Konfiguracja loggingu
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(funcName)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# ============================================================================
# Inicjalizacja środowiska
# ============================================================================

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
FONTS_DIR = BASE_DIR / 'fonts'
OUTPUT_DIR = BASE_DIR / 'output'

FONTS_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

logger.debug(f'Working directory: {BASE_DIR}')
logger.debug(f'Fonts directory: {FONTS_DIR}')
logger.debug(f'Output directory: {OUTPUT_DIR}')

# ============================================================================
# Konfiguracja Supabase (security: variables only, no hardcoding)
# ============================================================================

SUPABASE_URL: Optional[str] = os.getenv('SUPABASE_URL')
SUPABASE_KEY: Optional[str] = os.getenv('SUPABASE_KEY')

if not SUPABASE_URL:
    logger.critical('Environment variable SUPABASE_URL not set.')
    logger.info('Set it in .env file or system environment.')
    sys.exit(1)

if not SUPABASE_KEY:
    logger.critical('Environment variable SUPABASE_KEY not set.')
    logger.info('Set it in .env file or system environment.')
    sys.exit(1)

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    logger.info('✓ Supabase client initialized successfully.')
except Exception as e:
    logger.critical(f'Supabase initialization failed: {type(e).__name__}: {e}')
    sys.exit(1)

# ============================================================================
# Konfiguracja fontów DejaVu
# ============================================================================

FONTS_BASE_URL = 'https://raw.githubusercontent.com/dejavu-fonts/dejavu-fonts/master/ttf'

FONTS: dict[str, str] = {
    'DejaVuSans.ttf': f'{FONTS_BASE_URL}/DejaVuSans.ttf',
    'DejaVuSans-Bold.ttf': f'{FONTS_BASE_URL}/DejaVuSans-Bold.ttf',
}

REGISTERED_FONTS: dict[str, str] = {
    'DejaVuSans': 'DejaVuSans.ttf',
    'DejaVuSans-Bold': 'DejaVuSans-Bold.ttf',
}


# ============================================================================
# Funkcje
# ============================================================================

def download_fonts() -> bool:
    """Pobiera fonty DejaVu z repozytorium GitHub.

    Sprawdza czy fonty istnieją lokalnie. Jeśli nie, pobiera je z GitHub.
    W przypadku błędu pobierania, zwraca False.

    Returns:
        bool: True, jeśli wszystkie fonty dostępne; False w razie błędu.
    """
    logger.info('Checking fonts...')

    for filename, url in FONTS.items():
        font_path = FONTS_DIR / filename

        if font_path.exists():
            size_kb = font_path.stat().st_size / 1024
            logger.info(f'  ✓ {filename} found locally ({size_kb:.1f} KB)')
            continue

        logger.info(f'  ↓ Downloading {filename}...')
        try:
            urllib.request.urlretrieve(url, str(font_path))
            size_kb = font_path.stat().st_size / 1024
            logger.info(f'  ✓ {filename} downloaded ({size_kb:.1f} KB)')

        except urllib.error.URLError as e:
            logger.error(f'  ✗ Network error downloading {filename}: {e}')
            return False

        except Exception as e:
            logger.error(
                f'  ✗ Unexpected error downloading {filename}: '
                f'{type(e).__name__}: {e}'
            )
            return False

    logger.info('All fonts ready.')
    return True


def register_fonts() -> bool:
    """Rejestruje fonty DejaVu w reportlab.pdfmetrics.

    Operacja wymagana do używania DejaVuSans w generowanych PDF.
    Brak rejestracji = brak fontów w PDF.

    Returns:
        bool: True, jeśli sukces; False w razie błędu.
    """
    logger.info('Registering fonts in reportlab...')

    for font_name, filename in REGISTERED_FONTS.items():
        font_path = FONTS_DIR / filename

        if not font_path.exists():
            logger.error(f'  ✗ Font file not found: {font_path}')
            return False

        try:
            pdfmetrics.registerFont(TTFont(font_name, str(font_path)))
            logger.info(f'  ✓ {font_name} registered')

        except Exception as e:
            logger.error(
                f'  ✗ Failed to register {font_name}: '
                f'{type(e).__name__}: {e}'
            )
            return False

    logger.info('Font registration complete.')
    return True


def generate_aquastart_pdf() -> bool:
    """Generuje PDF z parametrami wody dla systemu AquaStart.

    Zawartość PDF:
    - Tytuł i nagłówek (DejaVuSans-Bold 22pt)
    - Polskie znaki diakrytyczne
    - Typografia premium: cudzysłowy „...", półpauz, indeksy chemiczne
    - Zakresy temperatur z symbolami

    Sygnatura PDF: %PDF-1.4 (automatycznie przez reportlab)

    Returns:
        bool: True, jeśli wygenerowany i zapisany; False w razie błędu.
    """
    # Pobranie fontów
    if not download_fonts():
        logger.error('Font download failed. Aborting.')
        return False

    # Rejestracja fontów
    if not register_fonts():
        logger.error('Font registration failed. Aborting.')
        return False

    filename = 'AquaStart_Parametry.pdf'
    file_path = OUTPUT_DIR / filename

    logger.info(f'Generating PDF: {filename}')

    try:
        # Utworzenie canvas (reportlab)
        c = canvas.Canvas(str(file_path), pagesize=A4)

        # Nagłówek
        c.setFont('DejaVuSans-Bold', 22)
        c.drawString(50, 770, 'AquaStart: Parametry Wody')

        # Separator
        c.setLineWidth(0.5)
        c.line(50, 765, 550, 765)

        # Zawartość (DejaVuSans Regular 11pt)
        c.setFont('DejaVuSans', 11)
        y_position = 740

        # Sekcja 1: Polskie znaki
        c.drawString(50, y_position, 'Polskie znaki diakrytyczne:')
        y_position -= 20
        c.drawString(50, y_position, 'ą ć ę ł ń ó ś ź ż')
        y_position -= 30

        # Sekcja 2: Typografia
        c.drawString(50, y_position, 'Zasada Akwarysty:')
        y_position -= 18
        c.drawString(50, y_position, '„Złota zasada akwarysty” – umiar w zarządzaniu.')
        y_position -= 30

        # Sekcja 3: Chemia
        c.drawString(50, y_position, 'Związki chemiczne w akwarium:')
        y_position -= 18
        c.drawString(50, y_position, 'Amoniak: NH₃  |  Dwutlenek węgla: CO₂')
        y_position -= 18
        c.drawString(50, y_position, 'Tlenek azotu: NO₂  |  Wodór: H₂  |  Tlen: O₂')
        y_position -= 30

        # Sekcja 4: Temperatura
        c.drawString(50, y_position, 'Temperatura optymalna:')
        y_position -= 18
        c.drawString(
            50,
            y_position,
            'Zakres roboczy: 24°C–26°C (dla większości gatunków)'
        )
        y_position -= 18
        c.drawString(50, y_position, 'Maksimum awaryjne: do 28°C')
        y_position -= 30

        # Sekcja 5: Zakresy pH
        c.drawString(50, y_position, 'Zakresy pH:')
        y_position -= 18
        c.drawString(50, y_position, 'Słodkowodne: pH 6,5–7,5')
        y_position -= 18
        c.drawString(50, y_position, 'Słonawe: pH 7,5–8,5')

        # Stopka
        c.setFont('DejaVuSans', 8)
        c.drawString(
            50,
            30,
            f'PDF signature: %PDF-1.4 | Generated: AquaStart v{__version__}'
        )

        c.save()
        logger.info(f'✓ PDF generated: {file_path}')

    except Exception as e:
        logger.error(
            f'PDF generation failed: {type(e).__name__}: {e}',
            exc_info=True
        )
        return False

    # Zapis metadanych do Supabase
    logger.info('Saving metadata to Supabase...')
    try:
        response = supabase.table('pdf_publications').insert({
            'title': 'AquaStart: Parametry Wody',
            'type': 'E-book',
            'file_url': str(file_path),
            'status': 'completed',
            'version': __version__,
        }).execute()

        if response.data:
            logger.info(f'✓ Database record created: {len(response.data)} row(s)')
        else:
            logger.warning('⚠ Database response empty, but no error.')

        return True

    except Exception as e:
        logger.error(
            f'Database write failed: {type(e).__name__}: {e}',
            exc_info=True
        )
        # Note: PDF już wygenerowany lokalnie, ale metadata nie zapisana
        return False


# ============================================================================
# Main
# ============================================================================

def main() -> int:
    """Punkt wejścia aplikacji.

    Returns:
        int: 0 (sukces) lub 1 (błąd).
    """
    logger.info('=' * 70)
    logger.info(f'AquaStart PDF Generator v{__version__}')
    logger.info('=' * 70)

    success = generate_aquastart_pdf()

    if success:
        logger.info('=' * 70)
        logger.info('✓ Process completed successfully.')
        logger.info('=' * 70)
        return 0
    else:
        logger.error('=' * 70)
        logger.error('✗ Process failed. See logs above.')
        logger.error('=' * 70)
        return 1


if __name__ == '__main__':
    sys.exit(main())
