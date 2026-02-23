#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AquaStart PDF Generator - Production v1.0.0
"""AquaStart PDF Generator - Production v1.0.0
Moduł generdu raportów PDF dla systemu zarządzania akwariami High-Tech.
Integracja z bazą danych Supabase i obsługa fontów DejaVu.mi High-Tech.
Integracja z bazą danych Supabase i obsługa fontów DejaVu.
Wymagania:
    - reportlab>=4.0.9
    - supabase>=2.0.49
    - python-dotenv>=1.0.0
    - python-dotenv>=1.0.0
Zmienne środowiskowe (.env):
    SUPABASE_URL (str): URL projektu Supabase
    SUPABASE_KEY (str): Klucz publiczny Supabase (anon/public)
    SUPABASE_KEY (str): Klucz publiczny Supabase (anon/public)
Użycie:
    python3 pdf_generator.py
""" python3 pdf_generator.py
"""
import logging
import osgging
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetimefrom typing import Optional
from dotenv import load_dotenv
import json

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscapert TTFont
from reportlab.lib.units import mms
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFontfrom supabase.client import Client
from reportlab.lib.colors import HexColor, Color
from reportlab.platypus import Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle__author__ = 'AquaStart'
import supabase
=======================================================
# ============================================================================
# KONFIGURACJA LOGOWANIA# ============================================================================
# ============================================================================

def setup_logging() -> logging.Logger:
    """Konfiguruje system logowania z file i console handlerami."""elname)-8s | %(funcName)s | %(message)s',
    log_dir = Path(__file__).parent / "logs"   datefmt='%Y-%m-%d %H:%M:%S'
    log_dir.mkdir(exist_ok=True)
    logger = logging.getLogger(__name__)
    log_file = log_dir / datetime.now().strftime("pdf_generator_%Y%m%d_%H%M%S.log")
    ====================================================
    logging.basicConfig(
        level=logging.INFO,# ============================================================================
        format='%(asctime)s - %(name)s - %(levelname)s - [%(funcName)s:%(lineno)d] - %(message)s',
        handlers=[load_dotenv()
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)lve().parent
        ]
    )OUTPUT_DIR = BASE_DIR / 'output'
    
    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized, log file: {log_file}")OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    return logger
)
logger = setup_logging()
logger.debug('Output directory: %s', OUTPUT_DIR)
# ============================================================================
# REJESTRACJA FONTÓW DEJAVU (OBOWIĄZKOWE DLA PDF)=============
# ============================================================================
# ============================================================================
FONTS_DIR = Path(__file__).parent / "fonts"
FONTS_DIR.mkdir(exist_ok=True)
SUPABASE_KEY: Optional[str] = os.getenv('SUPABASE_KEY')
def _register_dejavu_fonts() -> bool:
    """
    Rejestruje fonty DejaVu z obsługą fallback.t.')
    ('Set it in .env file or system environment.')
    Returns:    sys.exit(1)
        True jeśli co najmniej jeden font został zarejestrowany, False w przeciwnym razie
    """
    fonts_registered = Falset.')
    ('Set it in .env file or system environment.')
    # Definicje fontów    sys.exit(1)
    font_definitions = {
        'DejaVuSans': str(FONTS_DIR / "DejaVuSans.ttf"),
        'DejaVuSans-Bold': str(FONTS_DIR / "DejaVuSans-Bold.ttf"),Y)
        'DejaVuSans-Oblique': str(FONTS_DIR / "DejaVuSans-Oblique.ttf"),abase client initialized successfully.')
        'DejaVuSans-BoldOblique': str(FONTS_DIR / "DejaVuSans-BoldOblique.ttf"),
    }ical('Supabase initialization failed: %s: %s', type(e).__name__, e)
        sys.exit(1)
    for font_name, font_path in font_definitions.items():
        try:==================================================
            if Path(font_path).exists():
                pdfmetrics.registerFont(TTFont(font_name, font_path))# ============================================================================
                logger.info(f"✓ Font zarejestrowany: {font_name}")
                fonts_registered = True
            else:   'https://raw.githubusercontent.com/dejavu-fonts/dejavu-fonts/master/ttf'
                logger.warning(f"⚠ Font file nie znaleziony: {font_path}"))
        except Exception as e:
            logger.error(f"✗ Błąd rejestracji fontu {font_name}: {e}")
    
    if not fonts_registered:   'DejaVuSans-Bold.ttf': f'{FONTS_BASE_URL}/DejaVuSans-Bold.ttf',
        logger.critical("Brak zarejestrowanych fontów DejaVu!")}
    
    return fonts_registered{

_register_dejavu_fonts()   'DejaVuSans-Bold': 'DejaVuSans-Bold.ttf',
}
# ============================================================================
# KONFIGURACJA SUPABASE
# =================================================================================================================================================

def initialize_supabase() -> Optional[supabase.Client]:# ============================================================================
    """
    Inicjalizuje klienta Supabase z walidacją zmiennych środowiskowych.
        """Pobiera fonty DejaVu z repozytorium GitHub.
    Returns:
        Klient Supabase lub None w przypadku błędu nie, pobiera je z GitHub.
    """    W przypadku błędu pobierania, zwraca False.
    load_dotenv(Path(__file__).parent / ".env")
    
    SUPABASE_URL = os.getenv('SUPABASE_URL') bool: True, jeśli wszystkie fonty dostępne; False w razie błędu.
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')
        logger.info('Checking fonts...')
    if not SUPABASE_URL:
        logger.error("SUPABASE_URL nie ustawiony w zmiennych środowiskowych")
        return None        font_path = FONTS_DIR / filename
    
    if not SUPABASE_KEY:
        logger.error("SUPABASE_KEY nie ustawiony w zmiennych środowiskowych")
        return Nonenfo('  ✓ %s found locally (%.1f KB)', filename, size_kb)
                continue
    try:
        client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)er.info('  ↓ Downloading %s...', filename)
        logger.info("✓ Połączenie z Supabase nawiązane")
        return clientpath))
    except Exception as e:
        logger.error(f"✗ Błąd połączenia Supabase: {e}", exc_info=True)            logger.info('  ✓ %s downloaded (%.1f KB)', filename, size_kb)
        return None

supabase_client = initialize_supabase()('  ✗ Network error downloading %s: %s', filename, e)
            return False
# ============================================================================
# KLASA GENERATORA PDFas e:
# ============================================================================
pected error downloading %s: %s: %s',
class PDFGenerator:
    """pe(e).__name__,
    Generator profesjonalnych raportów PDF dla AquaStart.   e,
    Obsługuje: raporty jakości wody, harmonogramy pielęgnacji, analizy trendu.
    """            return False
    
    DEFAULT_FONT = "DejaVuSans"('All fonts ready.')
    DEFAULT_FONT_BOLD = "DejaVuSans-Bold"    return True
    COLOR_PRIMARY = HexColor("#2563EB")
    COLOR_ACCENT = HexColor("#10B981")
    COLOR_WARNING = HexColor("#F59E0B")
    COLOR_DANGER = HexColor("#EF4444")    """Rejestruje fonty DejaVu w reportlab.pdfmetrics.
    COLOR_TEXT = HexColor("#1F2937")
    COLOR_LIGHT = HexColor("#F3F4F6")ans w generowanych PDF.
        Brak rejestracji = brak fontów w PDF.
    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True) bool: True, jeśli sukces; False w razie błędu.
        self.logger = logger
        logger.info('Registering fonts in reportlab...')
    def _sanitize_text(self, text: str) -> str:
        """Sanityzuje tekst z potencjalnych zagrożeń bezpieczeństwa."""D_FONTS.items():
        if not isinstance(text, str):        font_path = FONTS_DIR / filename
            text = str(text)
        # Usunięcie kontrolnych znaków Unicode (poza whitespace)
        text = ''.join(('  ✗ Font file not found: %s', font_path)
            char for char in text             return False
            if ord(char) >= 32 or char in '\n\t\r'
        )
        return text.strip()tr(font_path)))
                logger.info('  ✓ %s registered', font_name)
    def _format_chemical_symbols(self, text: str) -> str:
        """Formatuje symbole chemiczne z indeksami."""as e:
        replacements = {
            'NH3': 'NH₃',d to register %s: %s: %s',
            'CO2': 'CO₂',
            'NO2': 'NO₂',pe(e).__name__,
            'NO3': 'NO₃',   e,
            'H2O': 'H₂O',
            'O2': 'O₂',            return False
        }
        for old, new in replacements.items():('Font registration complete.')
            text = text.replace(old, new)    return True
        return text
    
    def _format_polish_typography(self, text: str) -> str:
        """Formatuje tekst zgodnie z polską typografią."""    """Generuje PDF z parametrami wody dla systemu AquaStart.
        # Zmiana cudzysłowów na polskie
        text = text.replace('"', '„').replace('"', '"')
        if text.count('„') > text.count('"'):ns-Bold 22pt)
            parts = text.split('„')
            text = '„'.join(parts[:-1]) + '„' + parts[-1] „...”, półpauzy, indeksy chemiczne
        return text    - Zakresy temperatur z symbolami
    
    def generate_water_quality_report(    Sygnatura PDF: %PDF-1.4 (automatycznie przez reportlab)
        self,
        tank_id: str,
        tank_name: str, bool: True, jeśli wygenerowany i zapisany; False w razie błędu.
        parameters: Dict[str, Any],
        date_measured: Optional[str] = None,
        output_filename: Optional[str] = None('Font download failed. Aborting.')
    ) -> Optional[str]:        return False
        """
        Generuje profesjonalny raport jakości wody w PDF.
        ('Font registration failed. Aborting.')
        Args:        return False
            tank_id: ID zbiornika (np. 'tank_001')
            tank_name: Nazwa zbiornika (np. 'Główny zbiornik')df'
            parameters: Słownik parametrów {nazwa: wartość}    file_path = OUTPUT_DIR / filename
            date_measured: Data pomiaru (ISO format, default: teraz)
            output_filename: Niestandardowa nazwa pliku wyjściowego    logger.info('Generating PDF: %s', filename)
        
        Returns:
            Ścieżka do wygenerowanego pliku lub None w przypadku błędu        c = canvas.Canvas(str(file_path), pagesize=A4)
        """
        try:
            # Walidacja wejścia        c.drawString(50, 770, 'AquaStart: Parametry Wody')
            if not tank_id or not isinstance(tank_id, str):
                raise ValueError("tank_id musi być niepustym stringiem")
            if not tank_name or not isinstance(tank_name, str):        c.line(50, 765, 550, 765)
                raise ValueError("tank_name musi być niepustym stringiem")
            if not isinstance(parameters, dict) or not parameters:uSans', 11)
                raise ValueError("parameters musi być niepustym słownikiem")        y_position = 740
            
            # Sanityzacja y_position, 'Polskie znaki diakrytyczne:')
            tank_id = self._sanitize_text(tank_id)
            tank_name = self._sanitize_text(tank_name) y_position, 'ą ć ę ł ń ó ś ź ż')
                    y_position -= 30
            # Generowanie nazwy pliku
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S") y_position, 'Zasada Akwarysty:')
            filename = output_filename or f"raport_jakosciowy_{tank_id}_{timestamp}.pdf" 18
            filepath = self.output_dir / filenametring(
            
            # Utworzenie Canvas
            c = canvas.Canvas(str(filepath), pagesize=A4)   '„Złota zasada akwarysty” – umiar w zarządzaniu.',
            width, height = A4
                    y_position -= 30
            # Sprawdzenie, czy sygnatura PDF jest obecna
            self.logger.info(f"Generowanie PDF: {filename}") y_position, 'Związki chemiczne w akwarium:')
            
            # ==== NAGŁÓWEK ==== y_position, 'Amoniak: NH₃  |  Dwutlenek węgla: CO₂')
            c.setFillColor(self.COLOR_PRIMARY)
            c.rect(0, height - 50*mm, width, 50*mm, fill=1, stroke=0) y_position, 'Tlenek azotu: NO₂  |  Wodór: H₂  |  Tlen: O₂')
                    y_position -= 30
            c.setFillColor(HexColor("#FFFFFF"))
            c.setFont(self.DEFAULT_FONT_BOLD, 24) y_position, 'Temperatura optymalna:')
            c.drawString(20*mm, height - 28*mm, "AquaStart - Raport Jakości Wody") 18
            tring(
            c.setFont(self.DEFAULT_FONT, 11)
            c.drawString(20*mm, height - 38*mm, f"Zbiornik: {tank_name}")
            c.drawString(20*mm, height - 43*mm, f"ID: {tank_id}")   'Zakres roboczy: 24°C–26°C (dla większości gatunków)',
            
            date_str = date_measured or datetime.now().strftime('%d.%m.%Y %H:%M:%S')
            c.drawString(width - 80*mm, height - 28*mm, f"Data: {date_str}") y_position, 'Maksimum awaryjne: do 28°C')
                    y_position -= 30
            # ==== INFORMACJE OGÓLNE ====
            y_pos = height - 60*mm y_position, 'Zakresy pH:')
            c.setFillColor(self.COLOR_TEXT)
            c.setFont(self.DEFAULT_FONT_BOLD, 12) y_position, 'Słodkowodne: pH 6,5–7,5')
            c.drawString(20*mm, y_pos, "Parametry Wodne:")
                    c.drawString(50, y_position, 'Słonawe: pH 7,5–8,5')
            # ==== TABELA PARAMETRÓW ====
            y_pos -= 8*mmjaVuSans', 8)
            c.setFont(self.DEFAULT_FONT, 10)tring(
            
            param_list = []
            for param_name, param_value in parameters.items():   f'PDF signature: %PDF-1.4 | Generated: AquaStart v{__version__}',
                clean_name = self._sanitize_text(str(param_name))        )
                clean_value = self._sanitize_text(str(param_value))
                
                # Formatowanie symboli chemicznych        logger.info('✓ PDF generated: %s', file_path)
                clean_value = self._format_chemical_symbols(clean_value)
                as e:
                param_list.append((clean_name, clean_value))
            ailed: %s: %s',
            # Rysowanie parametrów w kolumnach (2 kolumny)pe(e).__name__,
            col_width = width / 2 - 40*mm
            col1_x = 20*mm   exc_info=True,
            col2_x = width / 2 + 10*mm
                    return False
            for idx, (name, value) in enumerate(param_list):
                is_right_col = (idx % 2) == 1er.info('Saving metadata to Supabase...')
                x_pos = col2_x if is_right_col else col1_x
                ns').insert({
                if is_right_col and idx % 2 == 1:rt: Parametry Wody',
                    y_pos -= 6*mm
                ath),
                c.drawString(x_pos, y_pos, f"• {name}:")
                c.drawString(x_pos + 50*mm, y_pos, str(value))': __version__,
                    }).execute()
            # ==== SEKCJA REKOMENDACJI ====
            y_pos -= 20*mm
            c.setFillColor(self.COLOR_LIGHT)ogger.info('✓ Database record created: %s row(s)', len(response.data))
            c.rect(20*mm, y_pos - 30*mm, width - 40*mm, 30*mm, fill=1, stroke=1)
                        logger.warning('⚠ Database response empty, but no error.')
            c.setFillColor(self.COLOR_TEXT)
            c.setFont(self.DEFAULT_FONT_BOLD, 11)        return True
            c.drawString(25*mm, y_pos - 8*mm, "Rekomendacje:")
            as e:
            c.setFont(self.DEFAULT_FONT, 10)
            recommendations = [ailed: %s: %s',
                "• Regularne zmiany wody (30% co 7 dni)",pe(e).__name__,
                "• Monitorowanie parametrów minimum 2x w tygodniu",
                "• Utrzymanie stałej temperatury (23–26°C)",   exc_info=True,
                "• Czyszczenie filtra co 14 dni",
            ]        return False
            
            rec_y = y_pos - 15*mm
            for rec in recommendations:
                c.drawString(25*mm, rec_y, rec)    """Punkt wejścia aplikacji.
                rec_y -= 5*mm
            
            # ==== STOPKA ==== int: 0 (sukces) lub 1 (błąd).
            c.setFont(self.DEFAULT_FONT, 8)
            c.setFillColor(HexColor("#999999"))
            c.drawString(t PDF Generator v%s', __version__)
                20*mm,    logger.info('=' * 70)
                15*mm,
                f"Wygenerowano przez AquaStart PDF Generator | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"    success = generate_aquastart_pdf()
            )
            
            c.drawString(width - 80*mm, 15*mm, "Strona 1 z 1")
            s completed successfully.')
            # Zapisanie PDFnfo('=' * 70)
            c.save()        return 0
            self.logger.info(f"✓ PDF wygenerowany pomyślnie: {filepath}")
            
            return str(filepath)s failed. See logs above.')
        rror('=' * 70)
        except ValueError as e:    return 1
            self.logger.error(f"✗ Błąd walidacji: {e}")
            return None
        except Exception as e:in__':
            self.logger.error(f"✗ Błąd generowania PDF: {e}", exc_info=True)    sys.exit(main())













































































































































































































































































































    sys.exit(main())if __name__ == "__main__":    return 0        logger.info("=" * 80)    logger.info("✓ Wszystkie testy PRZESZŁY – System gotowy do produkcji")    logger.info("\n" + "=" * 80)            return 1        logger.error("✗ TEST 3 NIEUDANY")    else:        logger.info(f"✓ TEST 3 PRZESZEDŁ: {pdf_path_3}")    if pdf_path_3:        )        daily_data=test_daily_data        tank_name="Główny zbiornik",        tank_id="tank_001",    pdf_path_3 = generator.generate_monthly_analytics_report(        ]        },            "amoniak": 0.05,            "temperatura": 25.0,            "pH": 7.2,            "data": "2026-02-23",        {        },            "amoniak": 0.08,            "temperatura": 24.8,            "pH": 7.3,            "data": "2026-01-08",        {        },            "amoniak": 0.1,            "temperatura": 24.5,            "pH": 7.2,            "data": "2026-01-01",        {    test_daily_data = [    logger.info("\n[TEST 3] Generowanie raportu analitycznego...")    # ==== TEST 3: Raport Analityczny ====            return 1        logger.error("✗ TEST 2 NIEUDANY")    else:        logger.info(f"✓ TEST 2 PRZESZEDŁ: {pdf_path_2}")    if pdf_path_2:        )        maintenance_tasks=test_maintenance        tank_id="tank_001",    pdf_path_2 = generator.generate_maintenance_schedule(        ]        },            "wykonane": True            "data_ostatniej": "2026-02-23",            "okres": "2x w tygodniu (3–4 dni)",            "nazwa": "Test parametrów podstawowych",        {        },            "wykonane": False            "data_ostatniej": "2026-02-01",            "okres": "Co miesiąc (30 dni)",            "nazwa": "Inspekcja urządzeń i lamp UV",        {        },            "wykonane": False            "data_ostatniej": "2026-01-23",            "okres": "Co miesiąc (30 dni)",            "nazwa": "Wymiana wkładu węglowego",        {        },            "wykonane": True            "data_ostatniej": "2026-02-16",            "okres": "Co 2 tygodnie (14 dni)",            "nazwa": "Czyszczenie filtra",        {        },            "wykonane": True            "data_ostatniej": "2026-02-23",            "okres": "Co tydzień (7 dni)",            "nazwa": "Zmiana wody (30%)",        {    test_maintenance = [    logger.info("\n[TEST 2] Generowanie harmonogramu pielęgnacji...")    # ==== TEST 2: Harmonogram Pielęgnacji ====            return 1        logger.error("✗ TEST 1 NIEUDANY")    else:        logger.info(f"✓ TEST 1 PRZESZEDŁ: {pdf_path_1}")    if pdf_path_1:        )        parameters=test_water_params        tank_name="Główny zbiornik akwariowy",        tank_id="tank_001",    pdf_path_1 = generator.generate_water_quality_report(        }        "Conductivity": "380 µS/cm",        "Azotany (NO₃)": "25 mg/L",        "Azotyn (NO₂)": "0 mg/L",        "Amoniak (NH₃)": "< 0.25 mg/L",        "Twardość węglanowa (KH)": "6 °",        "Twardość ogólna (GH)": "8 °",        "Temperatura": "24.5°C",        "pH": "7.2 – 7.4",    test_water_params = {    logger.info("\n[TEST 1] Generowanie raportu jakości wody...")    # ==== TEST 1: Raport Jakości Wody ====        generator = PDFGenerator(output_dir="output")        logger.info("=" * 80)    logger.info("AquaStart PDF Generator – Initialization")    logger.info("=" * 80)    """Główny punkt wejścia z testami."""def main() -> int:# ============================================================================# CLI INTERFACE# ============================================================================            return None            self.logger.error(f"✗ Błąd generowania raportu analitycznego: {e}", exc_info=True)        except Exception as e:                    return str(filepath)                        self.logger.info(f"✓ Raport analityczny wygenerowany: {filepath}")            c.save()                        c.drawString(20*mm, 15*mm, f"© 2026 AquaStart | Wygenerowano: {datetime.now().strftime('%Y-%m-%d')}")            c.setFillColor(HexColor("#999999"))            c.setFont(self.DEFAULT_FONT, 8)            # Stopka                            y_pos -= 6*mm                c.drawString(25*mm, y_pos, f"{stat_name}: {stat_value}")            for stat_name, stat_value in stats.items():                        }                "Ostatnie pomiary": daily_data[-1].get('data', 'N/A') if daily_data else "N/A",                "Pierwsze pomiary": daily_data[0].get('data', 'N/A') if daily_data else "N/A",                "Liczba pomiarów": len(daily_data),            stats = {                        c.setFont(self.DEFAULT_FONT, 10)            y_pos -= 10*mm                        c.drawString(20*mm, y_pos, "Statystyki Pomiarów:")            c.setFont(self.DEFAULT_FONT_BOLD, 12)            c.setFillColor(self.COLOR_TEXT)            y_pos = height - 55*mm            # Statystyki                        c.drawString(20*mm, height - 32*mm, f"Raport z: {datetime.now().strftime('%d.%m.%Y')}")            c.setFont(self.DEFAULT_FONT, 10)                        c.drawString(20*mm, height - 20*mm, f"Analityka Zbiornika – {tank_name}")            c.setFont(self.DEFAULT_FONT_BOLD, 24)            c.setFillColor(HexColor("#FFFFFF"))                        c.rect(0, height - 40*mm, width, 40*mm, fill=1, stroke=0)            c.setFillColor(self.COLOR_PRIMARY)            # Nagłówek                        width, height = landscape(A4)            c = canvas.Canvas(str(filepath), pagesize=landscape(A4))                        filepath = self.output_dir / filename            filename = output_filename or f"analityka_{tank_id}_{timestamp}.pdf"            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")                            raise ValueError("daily_data nie może być pusty")            if not daily_data:        try:        """            Ścieżka do PDF lub None        Returns:                    output_filename: Niestandardowa nazwa pliku            daily_data: Lista dziennych pomiarów            tank_name: Nazwa zbiornika            tank_id: ID zbiornika        Args:                Generuje miesięczny raport analityczny z trendami.        """    ) -> Optional[str]:        output_filename: Optional[str] = None        daily_data: List[Dict[str, Any]],        tank_name: str,        tank_id: str,        self,    def generate_monthly_analytics_report(                return None            self.logger.error(f"✗ Błąd generowania harmonogramu: {e}", exc_info=True)        except Exception as e:                    return str(filepath)                        self.logger.info(f"✓ Harmonogram wygenerowany: {filepath}")            c.save()                        )                f"Wygenerowano: {datetime.now().strftime('%Y-%m-%d')}"                15*mm,                20*mm,            c.drawString(            c.setFillColor(HexColor("#999999"))            c.setFont(self.DEFAULT_FONT, 8)            # Stopka                            y_pos -= 8*mm                                c.drawString(col_positions[3], y_pos - 4*mm, task_date)                c.drawString(col_positions[2], y_pos - 4*mm, task_period)                c.drawString(col_positions[1], y_pos - 4*mm, task_name)                c.drawString(col_positions[0], y_pos - 4*mm, str(idx))                c.setFillColor(self.COLOR_TEXT)                                c.rect(20*mm, y_pos - 6*mm, width - 40*mm, 6*mm, fill=1, stroke=1)                                    c.setFillColor(HexColor("#FFF9C4"))                else:                    c.setFillColor(HexColor("#E8F5E9"))                if completed:                # Kolorowanie wierszy                                completed = task.get('wykonane', False)                task_date = self._sanitize_text(str(task.get('data_ostatniej', 'N/A')))                task_period = self._sanitize_text(str(task.get('okres', 'N/A')))                task_name = self._sanitize_text(str(task.get('nazwa', 'N/A')))            for idx, task in enumerate(maintenance_tasks, 1):                        c.setFont(self.DEFAULT_FONT, 9)            y_pos -= 12*mm            # Wiersze danych                            c.drawString(col_positions[idx], y_pos - 6*mm, header)            for idx, header in enumerate(headers):                        headers = ["Lp.", "Zadanie", "Okres", "Ostatnia realizacja"]            col_positions = [25*mm, 60*mm, 130*mm, 170*mm]            c.setFont(self.DEFAULT_FONT_BOLD, 10)            c.setFillColor(self.COLOR_TEXT)                        c.rect(20*mm, y_pos - 8*mm, width - 40*mm, 8*mm, fill=1, stroke=1)            c.setFillColor(self.COLOR_LIGHT)            # Nagłówek tabeli                        y_pos = height - 55*mm            # Tabela zadań                        c.drawString(20*mm, height - 32*mm, f"Zbiornik ID: {tank_id} | Data: {datetime.now().strftime('%d.%m.%Y')}")            c.setFont(self.DEFAULT_FONT, 10)                        c.drawString(20*mm, height - 20*mm, "Harmonogram Pielęgnacji Zbiornika")            c.setFont(self.DEFAULT_FONT_BOLD, 22)            c.setFillColor(HexColor("#FFFFFF"))                        c.rect(0, height - 40*mm, width, 40*mm, fill=1, stroke=0)            c.setFillColor(self.COLOR_PRIMARY)            # Nagłówek                        width, height = A4            c = canvas.Canvas(str(filepath), pagesize=A4)                        filepath = self.output_dir / filename            filename = output_filename or f"harmonogram_{tank_id}_{timestamp}.pdf"            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")                            raise ValueError("maintenance_tasks musi być niepustą listą")            if not isinstance(maintenance_tasks, list) or not maintenance_tasks:        try:        """            Ścieżka do PDF lub None w przypadku błędu        Returns:                    output_filename: Niestandardowa nazwa pliku            maintenance_tasks: Lista słowników {'nazwa': str, 'okres': str, 'data_ostatniej': str, 'wykonane': bool}            tank_id: ID zbiornika        Args:                Generuje harmonogram pielęgnacji zbiornika.        """    ) -> Optional[str]:        output_filename: Optional[str] = None        maintenance_tasks: List[Dict[str, Any]],        tank_id: str,        self,    def generate_maintenance_schedule(                return None