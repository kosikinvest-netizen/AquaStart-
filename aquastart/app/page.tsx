'use client';

import Link from 'next/link';

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 via-cyan-50 to-blue-100 p-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-blue-600 mb-4">🌊 AquaStart</h1>
          <p className="text-xl text-gray-600">Platform do zarządzania zasobami wodnymi</p>
        </div>

        {/* Status Board */}
        <div className="grid md:grid-cols-3 gap-6 mb-12">
          {/* Konfiguracja */}
          <div className="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition">
            <div className="text-4xl mb-3">⚙️</div>
            <h3 className="text-xl font-bold text-gray-800 mb-2">Konfiguracja</h3>
            <p className="text-gray-600 text-sm mb-4">Skonfiguruj klucze Supabase</p>
            <Link
              href="/setup"
              className="inline-block px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition text-sm"
            >
              Przejdź do setup →
            </Link>
          </div>

          {/* Test */}
          <div className="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition">
            <div className="text-4xl mb-3">✅</div>
            <h3 className="text-xl font-bold text-gray-800 mb-2">Test Połączenia</h3>
            <p className="text-gray-600 text-sm mb-4">Sprawdź czy wszystko działa</p>
            <Link
              href="/test-connection"
              className="inline-block px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 transition text-sm"
            >
              Uruchom test →
            </Link>
          </div>

          {/* Dokumentacja */}
          <div className="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition">
            <div className="text-4xl mb-3">📚</div>
            <h3 className="text-xl font-bold text-gray-800 mb-2">Dokumentacja</h3>
            <p className="text-gray-600 text-sm mb-4">Przeczytaj instrukcje i przykłady</p>
            <a
              href="https://github.com"
              className="inline-block px-4 py-2 bg-purple-600 text-white rounded hover:bg-purple-700 transition text-sm"
              target="_blank"
              rel="noopener noreferrer"
            >
              Otwórz docs →
            </a>
          </div>
        </div>

        {/* Quick Start */}
        <div className="bg-white rounded-lg shadow-lg p-8 mb-12">
          <h2 className="text-3xl font-bold text-gray-800 mb-6">🚀 Szybki Start (4 kroki)</h2>
          
          <div className="space-y-6">
            {/* Krok 1 */}
            <div className="flex gap-4">
              <div className="flex-shrink-0">
                <div className="flex items-center justify-center h-10 w-10 rounded-full bg-blue-600 text-white font-bold">
                  1
                </div>
              </div>
              <div className="flex-grow">
                <h3 className="text-lg font-semibold text-gray-800">Otwórz Supabase</h3>
                <p className="text-gray-600 mt-1">
                  Przejdź na{' '}
                  <a
                    href="https://app.supabase.com"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-600 underline hover:no-underline"
                  >
                    app.supabase.com
                  </a>
                  {' '}i pobierz klucze z Settings → API
                </p>
              </div>
            </div>

            {/* Krok 2 */}
            <div className="flex gap-4">
              <div className="flex-shrink-0">
                <div className="flex items-center justify-center h-10 w-10 rounded-full bg-blue-600 text-white font-bold">
                  2
                </div>
              </div>
              <div className="flex-grow">
                <h3 className="text-lg font-semibold text-gray-800">Wstaw klucze</h3>
                <p className="text-gray-600 mt-1">
                  Otwórz plik <code className="bg-gray-200 px-2 py-1 rounded text-sm">.env.local</code> i wklej klucze
                </p>
              </div>
            </div>

            {/* Krok 3 */}
            <div className="flex gap-4">
              <div className="flex-shrink-0">
                <div className="flex items-center justify-center h-10 w-10 rounded-full bg-blue-600 text-white font-bold">
                  3
                </div>
              </div>
              <div className="flex-grow">
                <h3 className="text-lg font-semibold text-gray-800">Uruchom SQL script</h3>
                <p className="text-gray-600 mt-1">
                  W Supabase → SQL Editor → New Query → wklej SQL (instrukcja w setup)
                </p>
              </div>
            </div>

            {/* Krok 4 */}
            <div className="flex gap-4">
              <div className="flex-shrink-0">
                <div className="flex items-center justify-center h-10 w-10 rounded-full bg-blue-600 text-white font-bold">
                  4
                </div>
              </div>
              <div className="flex-grow">
                <h3 className="text-lg font-semibold text-gray-800">Zrestartuj serwer</h3>
                <p className="text-gray-600 mt-1">
                  W terminalu: <code className="bg-gray-200 px-2 py-1 rounded text-sm">Ctrl+C</code> i{' '}
                  <code className="bg-gray-200 px-2 py-1 rounded text-sm">npm run dev</code>
                </p>
              </div>
            </div>
          </div>

          <div className="mt-8">
            <Link
              href="/setup"
              className="inline-block px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition font-bold"
            >
              Przejdź do szczegółowych instrukcji →
            </Link>
          </div>
        </div>

        {/* Info */}
        <div className="bg-cyan-50 border border-cyan-200 rounded-lg p-6">
          <h3 className="text-lg font-bold text-cyan-900 mb-2">💡 Potrzebujesz pomocy?</h3>
          <p className="text-cyan-900 mb-4">
            Po ukończeniu setupu możesz:
          </p>
          <ul className="text-cyan-900 space-y-2">
            <li>✅ Sprawdzić połączenie na stronie <Link href="/test-connection" className="underline">test-connection</Link></li>
            <li>📖 Przeczytać dokumentację w <code className="bg-white px-1">SUPABASE_README.md</code></li>
            <li>💻 Sprawdzić przykłady kodu w <code className="bg-white px-1">src/lib/supabase-examples.ts</code></li>
          </ul>
        </div>
      </div>
    </main>
  );
}
