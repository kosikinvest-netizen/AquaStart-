#!/bin/bash

set -e

echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║           AQUASTART QA AUDIT - FULL DEPLOYMENT                             ║"
echo "║                    Wersja: 1.0 | Data: $(date '+%Y-%m-%d %H:%M:%S')       ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"
echo ""

cd /workspaces/AquaStart-/aquastart

# KROK 1: Backup
echo "═══════════════════════════════════════════════════════════════════"
echo "KROK 1/8: Backup bieżących plików"
echo "═══════════════════════════════════════════════════════════════════"
if [ -f backend/pdf_generator.py ]; then
    cp backend/pdf_generator.py backend/pdf_generator.py.backup
    echo "✅ Backup: backend/pdf_generator.py.backup"
fi
echo ""

# KROK 2: Aktualizacja requirements.txt
echo "═══════════════════════════════════════════════════════════════════"
echo "KROK 2/8: Aktualizacja requirements.txt"
echo "═══════════════════════════════════════════════════════════════════"
cat > backend/requirements.txt << 'EOF'
supabase==2.10.0
python-dotenv==1.0.0
reportlab==4.0.9
requests==2.31.0
python-docx==0.8.11
EOF
echo "✅ Zaktualizowano requirements.txt (supabase 2.0.4 → 2.10.0)"
cat backend/requirements.txt
echo ""

# KROK 3: Deploy pdf_generator
echo "═══════════════════════════════════════════════════════════════════"
echo "KROK 3/8: Deploy pdf_generator.py"
echo "═══════════════════════════════════════════════════════════════════"
if [ -f backend/pdf_generator_v2.py ]; then
    cp backend/pdf_generator_v2.py backend/pdf_generator.py
    echo "✅ Wdrożono: pdf_generator_v2.py → pdf_generator.py"
    python3 -m py_compile backend/pdf_generator.py && echo "✅ Składnia Python OK"
elif [ -f backend/pdf_generator_FINAL.py ]; then
    cp backend/pdf_generator_FINAL.py backend/pdf_generator.py
    echo "✅ Wdrożono: pdf_generator_FINAL.py → pdf_generator.py"
    python3 -m py_compile backend/pdf_generator.py && echo "✅ Składnia Python OK"
else
    echo "⚠️  Używam istniejącego pdf_generator.py"
    python3 -m py_compile backend/pdf_generator.py && echo "✅ Składnia Python OK"
fi
echo ""

# KROK 4: Instalacja zależności
echo "═══════════════════════════════════════════════════════════════════"
echo "KROK 4/8: Instalacja zależności Python"
echo "═══════════════════════════════════════════════════════════════════"
pip install --quiet --upgrade pip
pip install -r backend/requirements.txt
echo "✅ Zainstalowane pakiety:"
pip list | grep -E "reportlab|supabase|python-dotenv|python-docx"
echo ""

# KROK 5: Konfiguracja .env
echo "═══════════════════════════════════════════════════════════════════"
echo "KROK 5/8: Konfiguracja plików środowiskowych"
echo "═══════════════════════════════════════════════════════════════════"

# Backend .env.example
if [ ! -f backend/.env.example ]; then
    cat > backend/.env.example << 'EOF'
# Supabase Configuration
# Get these values from: https://app.supabase.com/project/_/settings/api

SUPABASE_URL=your_supabase_url_here
SUPABASE_KEY=your_supabase_anon_key_here

# Optional: Supabase Service Role Key (for admin operations)
# WARNING: Keep this secret! Never commit to git!
# SUPABASE_SERVICE_KEY=your_service_role_key_here
EOF
    echo "✅ Utworzono backend/.env.example"
else
    echo "✅ backend/.env.example już istnieje"
fi

# Backend .env
if [ ! -f backend/.env ]; then
    cp backend/.env.example backend/.env
    echo "⚠️  Utworzono backend/.env - WYMAGANE: Dodaj klucze Supabase"
else
    echo "✅ backend/.env już istnieje"
fi

# Frontend .env.local
if [ ! -f .env.local ]; then
    cat > .env.local << 'EOF'
# Supabase Configuration (Frontend)
# Get from: https://app.supabase.com/project/_/settings/api

NEXT_PUBLIC_SUPABASE_URL=your_supabase_url_here
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key_here

# Server-side only (NEVER expose in client code)
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key_here
EOF
    echo "⚠️  Utworzono .env.local - WYMAGANE: Dodaj klucze Supabase"
else
    echo "✅ .env.local już istnieje"
fi
echo ""

# KROK 6: Test konfiguracji
echo "═══════════════════════════════════════════════════════════════════"
echo "KROK 6/8: Test konfiguracji środowiska"
echo "═══════════════════════════════════════════════════════════════════"
python3 backend/test_setup.py
echo ""

# KROK 7: Uprawnienia i struktura
echo "═══════════════════════════════════════════════════════════════════"
echo "KROK 7/8: Struktura katalogów i uprawnienia"
echo "═══════════════════════════════════════════════════════════════════"
chmod +x run_pdf.sh
mkdir -p backend/output backend/fonts
echo "✅ run_pdf.sh: executable"
echo "✅ backend/output/"
echo "✅ backend/fonts/"
echo ""

# KROK 8: Weryfikacja
echo "═══════════════════════════════════════════════════════════════════"
echo "KROK 8/8: Weryfikacja systemu"
echo "═══════════════════════════════════════════════════════════════════"
echo ""
echo "📁 Struktura backend/:"
tree -L 2 backend/ -I '__pycache__|*.pyc' 2>/dev/null || find backend -maxdepth 2 -type f | sort
echo ""
echo "📋 Status plików:"
for file in backend/{pdf_generator.py,test_setup.py,requirements.txt,.env.example,.env} run_pdf.sh .env.local; do
    if [ -f "$file" ]; then
        size=$(ls -lh "$file" | awk '{print $5}')
        echo "  ✅ $file ($size)"
    else
        echo "  ❌ $file - BRAK"
    fi
done
echo ""

echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║                     DEPLOYMENT ZAKOŃCZONY POMYŚLNIE                        ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"
echo ""
echo "🔑 KONFIGURACJA KLUCZY SUPABASE"
echo ""
echo "Otwórz Supabase Dashboard w przeglądarce:"
echo '  $BROWSER https://app.supabase.com/project/_/settings/api'
echo ""
echo "Następnie edytuj pliki konfiguracyjne:"
echo ""
echo "1. Backend (Python):"
echo "   nano backend/.env"
echo ""
echo "2. Frontend (Next.js):"
echo "   nano .env.local"
echo ""
echo "📖 Pełna dokumentacja: cat SUPABASE_README.md"
echo ""
echo "🚀 URUCHOMIENIE"
echo ""
echo "Backend (PDF Generator):"
echo "   ./run_pdf.sh"
echo ""
echo "Frontend (Next.js):"
echo "   npm install"
echo "   npm run dev"
echo ""
echo "✅ Wszystkie kroki z IMPLEMENTATION_CHECKLIST.txt wykonane!"
echo ""
