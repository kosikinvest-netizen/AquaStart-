#!/bin/bash
set -e

clear

echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║              AQUASTART - COMPLETE DEPLOYMENT (GitHub + Vercel + CI/CD)     ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"
echo ""

# KROK 1: Dodaj brakujące pliki
echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║                    KROK 1/3: DODAJ PLIKI NA GITHUB                         ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"
echo ""

git add -A
git commit -m "fix: Add all missing files to repository" || echo "ℹ️  No new files to commit"
git push origin main

echo "✅ Krok 1/3 zakończony"
sleep 2

# KROK 2: Deploy na Vercel
echo ""
echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║                    KROK 2/3: DEPLOY NA VERCEL                              ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"
echo ""

if ! command -v vercel &> /dev/null; then
    echo "📦 Instaluję Vercel CLI..."
    npm install -g vercel
fi

cat > vercel.json << 'VERCEL'
{
  "buildCommand": "npm run build",
  "devCommand": "npm run dev",
  "installCommand": "npm install"
}
VERCEL

echo "🌐 Deployuję na Vercel..."
vercel --prod --token $VERCEL_TOKEN 2>/dev/null || vercel --prod

echo "✅ Krok 2/3 zakończony"
sleep 2

# KROK 3: GitHub Actions
echo ""
echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║                    KROK 3/3: SKONFIGURUJ GITHUB ACTIONS                    ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"
echo ""

mkdir -p .github/workflows

cat > .github/workflows/test-backend.yml << 'WF1'
name: Test Backend
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - run: pip install -r backend/requirements.txt
      - run: python3 backend/test_setup.py
      - run: ./run_pdf.sh
      - run: test -f backend/output/AquaStart_Parametry.pdf
WF1

cat > .github/workflows/test-frontend.yml << 'WF2'
name: Test Frontend
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'
      - run: npm ci
      - run: npm run build
WF2

git add .github/
git commit -m "ci: Add GitHub Actions workflows"
git push origin main

echo "✅ Krok 3/3 zakończony"

echo ""
echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║                    ✅ COMPLETE DEPLOYMENT FINISHED                         ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"
echo ""
echo "🎉 Cały deployment ukończony!"
echo ""
echo "📊 Status:"
echo "   ✅ GitHub: Wszystkie pliki wdrożone"
echo "   ✅ Vercel: Frontend w produkcji"
echo "   ✅ CI/CD: GitHub Actions skonfigurowany"
echo ""
