#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Skrypt testowy do sprawdzenia konfiguracji.

Test konfiguracji AquaStart:
- Importy wymaganych bibliotek
- Konfiguracja Supabase
- Generowanie testowego PDF (DejaVuSans)
"""

import logging
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

from dotenv import load_dotenv
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent
FONTS_DIR = BASE_DIR / 'fonts'
OUTPUT_DIR = BASE_DIR / 'output'

FONTS_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

FONTS_BASE_URL = (
    'https://raw.githubusercontent.com/dejavu-fonts/dejavu-fonts/master/ttf'
)

FONTS: dict[str, str] = {
    'DejaVuSans.ttf': f'{FONTS_BASE_URL}/DejaVuSans.ttf',
    'DejaVuSans-Bold.ttf': f'{FONTS_BASE_URL}/DejaVuSans-Bold.ttf',
}


def download_fonts() -> bool:
    """Pobiera fonty DejaVu, jeśli nie istnieją lokalnie."""
    for filename, url in FONTS.items():
        font_path = FONTS_DIR / filename
        if font_path.exists():
            logger.info('✓ %s found locally', filename)
            continue

        logger.info('↓ Downloading %s...', filename)
        try:
            urllib.request.urlretrieve(url, str(font_path))
            logger.info('✓ %s downloaded', filename)
        except urllib.error.URLError as e:
            logger.error('✗ Network error downloading %s: %s', filename, e)
            return False
        except Exception as e:
            logger.error(
                '✗ Unexpected error downloading %s: %s: %s',
                filename,
                type(e).__name__,
                e,
            )
            return False

    return True


def register_fonts() -> bool:
    """Rejestruje DejaVuSans w reportlab."""
    try:
        pdfmetrics.registerFont(TTFont('DejaVuSans', str(FONTS_DIR / 'DejaVuSans.ttf')))
        pdfmetrics.registerFont(
            TTFont('DejaVuSans-Bold', str(FONTS_DIR / 'DejaVuSans-Bold.ttf'))
        )
        return True
    except Exception as e:
        logger.error('✗ Font registration failed: %s: %s', type(e).__name__, e)
        return False


def main() -> int:
    """Wykonuje testy konfiguracji."""
    logger.info('Test 1/3: Sprawdzanie importów...')
    logger.info('✓ reportlab zaimportowany')
    logger.info('✓ python-dotenv zaimportowany')

    logger.info('Test 2/3: Sprawdzanie zmiennych środowiskowych...')
    load_dotenv()
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')

    if supabase_url and supabase_key:
        logger.info('✓ SUPABASE_URL: %s...', supabase_url[:40])
        logger.info('✓ SUPABASE_KEY: %s...', supabase_key[:20])
    else:
        logger.warning('⚠ Supabase env vars missing (optional for tests).')

    logger.info('Test 3/3: Test generowania PDF (DejaVuSans)...')
    if not download_fonts():
        return 1
    if not register_fonts():
        return 1

    test_filename = OUTPUT_DIR / 'test_output.pdf'

    try:
        c = canvas.Canvas(str(test_filename))
        c.setFont('DejaVuSans', 12)
        c.drawString(100, 750, 'Test PDF - AquaStart')
        c.save()

        if test_filename.exists():
            file_size = test_filename.stat().st_size
            logger.info('✓ PDF wygenerowany: %s (%s bajtów)', test_filename, file_size)
            test_filename.unlink()
            logger.info('✓ Plik testowy usunięty')
        else:
            logger.error('✗ PDF nie został utworzony')
            return 1
    except Exception as e:
        logger.error('✗ Błąd generowania PDF: %s: %s', type(e).__name__, e)
        return 1

    logger.info('✅ Wszystkie testy zakończone pomyślnie!')
    return 0


if __name__ == '__main__':
    sys.exit(main())
