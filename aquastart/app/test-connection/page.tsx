'use client';

import { useState, useEffect } from 'react';
import { supabase } from '@/lib/supabase';

export default function TestConnection() {
  const [status, setStatus] = useState<{
    config: string;
    connection: string;
    tables: string;
    error?: string;
  }>({
    config: 'Sprawdzanie konfiguracji...',
    connection: 'Czekanie...',
    tables: 'Czekanie...',
  });

  useEffect(() => {
    async function testConnection() {
      try {
        // 1. Sprawdź zmienne środowiskowe
        const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
        const key = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

        if (!url || !key) {
          setStatus((prev) => ({
            ...prev,
            config: '❌ Brakuje zmiennych w .env.local!',
            error: 'Upewnij się że NEXT_PUBLIC_SUPABASE_URL i NEXT_PUBLIC_SUPABASE_ANON_KEY są ustawione',
          }));
          return;
        }

        setStatus((prev) => ({
          ...prev,
          config: `✅ Konfiguracja OK (URL: ${url.substring(0, 40)}...)`,
        }));

        // 2. Test połączenia
        const { data: healthData, error: healthError } = await supabase
          .from('profiles')
          .select('count');

        if (healthError) {
          // Może tabela nie istnieje jeszcze - to OK, znaczy że połączenie działa
          if (healthError.message.includes('no rows') || healthError.message.includes('does not exist')) {
            setStatus((prev) => ({
              ...prev,
              connection: '✅ Połączenie OK (serwer odpowiada)',
              tables: '⚠️ Tabela "profiles" nie istnieje - uruchom SQL script',
            }));
            return;
          }
          throw healthError;
        }

        setStatus((prev) => ({
          ...prev,
          connection: '✅ Połączenie OK!',
          tables: '✅ Tabela "profiles" istnieje',
        }));
      } catch (error: any) {
        setStatus((prev) => ({
          ...prev,
          connection: `❌ Błąd: ${error.message}`,
          error: error.message,
        }));
      }
    }

    testConnection();
  }, []);

  return (
    <main className="min-h-screen bg-gradient-to-b from-blue-50 to-blue-100 p-8">
      <div className="max-w-2xl mx-auto">
        <div className="bg-white rounded-lg shadow-lg p-8">
          <h1 className="text-4xl font-bold mb-8 text-blue-600">🌊 AquaStart - Test Połączenia</h1>

          <div className="space-y-6">
            {/* Konfiguracja */}
            <div className="border-l-4 border-blue-500 pl-4">
              <h2 className="text-lg font-semibold text-gray-800 mb-2">1️⃣ Konfiguracja</h2>
              <p className="text-gray-700">{status.config}</p>
            </div>

            {/* Połączenie */}
            <div className="border-l-4 border-green-500 pl-4">
              <h2 className="text-lg font-semibold text-gray-800 mb-2">2️⃣ Połączenie z Supabase</h2>
              <p className="text-gray-700">{status.connection}</p>
            </div>

            {/* Tabele */}
            <div className="border-l-4 border-purple-500 pl-4">
              <h2 className="text-lg font-semibold text-gray-800 mb-2">3️⃣ Baza Danych</h2>
              <p className="text-gray-700">{status.tables}</p>
            </div>

            {/* Error */}
            {status.error && (
              <div className="bg-red-50 border border-red-200 rounded p-4">
                <p className="text-red-800 text-sm">{status.error}</p>
              </div>
            )}

            {/* Instrukcje */}
            <div className="bg-blue-50 border border-blue-200 rounded p-6 mt-8">
              <h3 className="font-bold text-blue-900 mb-4">📝 Co robić jeśli test się nie powiódł?</h3>
              <ol className="space-y-3 text-blue-900">
                <li>
                  <strong>1. Sprawdź klucze:</strong> Otwórz{' '}
                  <code className="bg-white px-2 py-1 rounded">.env.local</code> i upewnij się że
                  klucze z Supabase są wklejone prawidłowo
                </li>
                <li>
                  <strong>2. Uruchom SQL script:</strong> W Supabase Dashboard → SQL Editor, wklej
                  poniższy script
                </li>
                <li>
                  <strong>3. Zrestartuj serwer:</strong> Ctrl+C w terminalu, potem <code>npm run dev</code>
                </li>
              </ol>
            </div>

            {/* Link do Supabase */}
            <a
              href="https://app.supabase.com"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-block mt-4 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
            >
              Otwórz Supabase Dashboard →
            </a>
          </div>
        </div>
      </div>
    </main>
  );
}
