"""Test konfiguracji środowiska AquaStart."""

import logging
import os
import sys
from pathlib import Path
from typing import Optional

# Konfiguracja logowania
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def test_imports() -> bool:
    """Test importów wymaganych bibliotek."""
    logger.info("Test 1/4: Sprawdzanie importów...")
    
    try:
        import reportlab
        logger.info("✓ reportlab zaimportowany")
    except ImportError as e:
        logger.error(f"✗ reportlab: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        logger.info("✓ python-dotenv zaimportowany")
    except ImportError as e:
        logger.error(f"✗ python-dotenv: {e}")
        return False
    
    try:
        import supabase
        logger.info("✓ supabase zaimportowany")
    except ImportError as e:
        logger.error(f"✗ supabase: {e}")
        return False
    
    try:
        import docx
        logger.info("✓ python-docx zaimportowany")
    except ImportError as e:
        logger.error(f"✗ python-docx: {e}")
        return False
    
    return True


def test_env_vars() -> bool:
    """Test zmiennych środowiskowych."""
    logger.info("Test 2/4: Sprawdzanie zmiennych środowiskowych...")
    
    from dotenv import load_dotenv
    
    # Ładowanie z backend/.env
    env_path = Path(__file__).parent / ".env"
    load_dotenv(env_path)
    
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    
    if not supabase_url:
        logger.error("✗ SUPABASE_URL nie ustawiony w .env")
        return False
    
    if supabase_url == "your_supabase_url_here":
        logger.warning("⚠ SUPABASE_URL zawiera placeholder - edytuj backend/.env")
        logger.info(f"  Current: {supabase_url[:50]}...")
    else:
        logger.info(f"✓ SUPABASE_URL: {supabase_url[:50]}...")
    
    if not supabase_key:
        logger.error("✗ SUPABASE_KEY nie ustawiony w .env")
        return False
    
    if supabase_key == "your_supabase_anon_key_here":
        logger.warning("⚠ SUPABASE_KEY zawiera placeholder - edytuj backend/.env")
        logger.info(f"  Current: {supabase_key[:30]}...")
    else:
        logger.info(f"✓ SUPABASE_KEY: {supabase_key[:30]}...")
    
    return True


def test_directories() -> bool:
    """Test struktury katalogów."""
    logger.info("Test 3/4: Sprawdzanie struktury katalogów...")
    
    base_dir = Path(__file__).parent
    
    required_dirs = {
        "output": base_dir / "output",
        "fonts": base_dir / "fonts",
    }
    
    all_ok = True
    for name, path in required_dirs.items():
        if path.exists():
            logger.info(f"✓ {name}/ istnieje")
        else:
            logger.warning(f"⚠ {name}/ nie istnieje - tworzę...")
            path.mkdir(parents=True, exist_ok=True)
            logger.info(f"✓ {name}/ utworzony")
    
    return all_ok


def test_pdf_generation() -> bool:
    """Test generowania prostego PDF z wbudowanym fontem."""
    logger.info("Test 4/4: Test generowania PDF (Helvetica)...")
    
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
        
        output_dir = Path(__file__).parent / "output"
        output_dir.mkdir(exist_ok=True)
        
        test_pdf = output_dir / "test_setup.pdf"
        
        # Użyj wbudowanego fontu Helvetica (nie wymaga pobierania)
        c = canvas.Canvas(str(test_pdf), pagesize=A4)
        c.setFont("Helvetica", 12)
        c.drawString(100, 750, "AquaStart PDF Generator - Test Setup")
        c.drawString(100, 730, "Environment: OK")
        c.drawString(100, 710, f"Date: {Path(__file__).stat().st_mtime}")
        c.save()
        
        logger.info(f"✓ Test PDF utworzony: {test_pdf}")
        logger.info(f"  Size: {test_pdf.stat().st_size} bytes")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ Błąd generowania PDF: {e}")
        return False


def main() -> int:
    """Główna funkcja testowa."""
    logger.info("=" * 70)
    logger.info("AquaStart - Test Konfiguracji Środowiska")
    logger.info("=" * 70)
    logger.info("")
    
    tests = [
        ("Importy", test_imports),
        ("Zmienne środowiskowe", test_env_vars),
        ("Struktura katalogów", test_directories),
        ("Generowanie PDF", test_pdf_generation),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            logger.error(f"✗ {name} - Nieoczekiwany błąd: {e}")
            results.append((name, False))
        logger.info("")
    
    logger.info("=" * 70)
    logger.info("PODSUMOWANIE")
    logger.info("=" * 70)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        logger.info(f"{status} - {name}")
    
    all_passed = all(result for _, result in results)
    
    if all_passed:
        logger.info("")
        logger.info("✅ Wszystkie testy zakończone pomyślnie!")
        logger.info("")
        logger.info("Następne kroki:")
        logger.info("1. Edytuj klucze Supabase (jeśli potrzeba):")
        logger.info("   nano backend/.env")
        logger.info("2. Wygeneruj PDF:")
        logger.info("   cd .. && ./run_pdf.sh")
        return 0
    else:
        logger.error("")
        logger.error("❌ Niektóre testy nie powiodły się")
        logger.error("Sprawdź logi powyżej i napraw problemy")
        return 1


if __name__ == "__main__":
    sys.exit(main())
