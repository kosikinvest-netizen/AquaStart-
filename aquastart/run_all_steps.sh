#!/bin/bash
set -e

clear

echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║              AQUASTART - DEPLOYMENT COMPLETE (5 KROKÓW)                    ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"
echo ""

# KROK 1
echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║                    KROK 1/5: WERYFIKACJA ŚRODOWISKA                        ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"
echo ""
python3 backend/test_setup.py
echo ""
read -p "Naciśnij Enter aby kontynuować do kroku 2..."

# KROK 2
echo ""
echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║                    KROK 2/5: GENEROWANIE PDF                               ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"
echo ""
./run_pdf.sh
echo ""
read -p "Naciśnij Enter aby kontynuować do kroku 3..."

# KROK 3
echo ""
echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║                    KROK 3/5: WERYFIKACJA PDF                               ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"
echo ""
if [ -f backend/output/AquaStart_Parametry.pdf ]; then
    ls -lh backend/output/AquaStart_Parametry.pdf
    file backend/output/AquaStart_Parametry.pdf
    echo ""
    echo "📖 Otwieranie PDF..."
    "$BROWSER" "file://$(pwd)/backend/output/AquaStart_Parametry.pdf"
    echo "✅ PDF otwarty"
else
    echo "❌ PDF nie został wygenerowany!"
    exit 1
fi
echo ""
read -p "Naciśnij Enter aby kontynuować do kroku 4..."

# KROK 4
echo ""
echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║                    KROK 4/5: INSTALACJA ZALEŻNOŚCI                         ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"
echo ""
if [ ! -d node_modules ]; then
    npm install
else
    echo "✅ node_modules już istnieją"
fi
echo ""
read -p "Naciśnij Enter aby kontynuować do kroku 5..."

# KROK 5
echo ""
echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║                    KROK 5/5: URUCHOMIENIE FRONTEND                         ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"
echo ""
echo "🌐 Uruchamiam dev server w tle..."
nohup npm run dev > dev-server.log 2>&1 &
DEV_PID=$!
echo "✅ Dev server PID: $DEV_PID"
sleep 5
"$BROWSER" http://localhost:3000

echo ""
echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║                         ✅ DEPLOYMENT COMPLETE                             ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"
echo ""
echo "Dev server PID: $DEV_PID"
echo "Logi: tail -f dev-server.log"
echo "Stop: pkill -f 'next dev'"
echo ""
