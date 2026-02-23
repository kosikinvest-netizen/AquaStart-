#!/bin/bash
# AquaStart PDF Generator - Entrypoint Script
# Uruchamia generator PDF z walidacją konfiguracji

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR" || exit 1

echo "=================================================="
echo "🚀 AquaStart PDF Generator"
echo "=================================================="
echo ""

# Sprawdzenie czy backend/.env istnieje
if [ ! -f backend/.env ]; then
    echo "❌ BŁĄD: Plik backend/.env nie znaleziony."
    echo ""
    echo "Instrukcja:"
    echo "  1. skopiuj: cp backend/.env.example backend/.env"
    echo "  2. edytuj:  backend/.env"
    echo "  3. wstaw swoje klucze Supabase"
    echo ""
    exit 1
fi

# Załaduj zmienne ze środowiska
set -a
source backend/.env
set +a

# Walidacja zmiennych
ERROR_COUNT=0

if [ -z "$SUPABASE_URL" ]; then
    echo "❌ Brakuje: SUPABASE_URL w backend/.env"
    ERROR_COUNT=$((ERROR_COUNT + 1))
fi

if [ -z "$SUPABASE_KEY" ]; then
    echo "❌ Brakuje: SUPABASE_KEY w backend/.env"
    ERROR_COUNT=$((ERROR_COUNT + 1))
fi

if [ $ERROR_COUNT -gt 0 ]; then
    echo ""
    echo "Popraw backend/.env i uruchom ponownie."
    exit 1
fi

echo "✓ Konfiguracja załadowana."
echo "  - SUPABASE_URL: ${SUPABASE_URL:0:40}..."
echo ""

# Sprawdzenie czy Python istnieje
if ! command -v python3 &> /dev/null; then
    echo "❌ BŁĄD: python3 nie znaleziony w PATH"
    exit 1
fi

echo "✓ Python3 znaleziony."
echo ""

# Uruchomienie generatora
cd backend
echo "▶ Uruchamianie: python3 pdf_generator.py"
echo ""

python3 pdf_generator.py
EXIT_CODE=$?

echo ""
if [ $EXIT_CODE -eq 0 ]; then
    echo "=================================================="
    echo "✅ Sukces!"
    echo "=================================================="
    exit 0
else
    echo "=================================================="
    echo "❌ Błąd! (exit code: $EXIT_CODE)"
    echo "=================================================="
    exit 1
fi

