'use client';

import Link from 'next/link';

export default function Setup() {
  return (
    <main className="min-h-screen bg-gradient-to-b from-blue-50 to-blue-100 p-8">
      <div className="max-w-3xl mx-auto">
        <div className="bg-white rounded-lg shadow-lg p-8">
          <h1 className="text-4xl font-bold mb-8 text-blue-600">🌊 AquaStart - Setup</h1>

          {/* Krok 1 */}
          <section className="mb-8 pb-8 border-b">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">Krok 1️⃣: Pobierz klucze Supabase</h2>
            <ol className="list-decimal pl-5 space-y-2 text-gray-700 mb-4">
              <li>Otwórz: <a href="https://app.supabase.com" target="_blank" rel="noopener noreferrer" className="text-blue-600 underline">app.supabase.com</a></li>
              <li>Zaloguj się lub utwórz konto (free)</li>
              <li>Kliknij: <strong>New Project</strong> (lub wybierz istniejący)</li>
              <li>Przejdź do: <strong>Settings</strong> → <strong>API</strong></li>
              <li>Skopiuj:
                <ul className="list-disc pl-5 mt-2 space-y-1">
                  <li><strong>Project URL</strong> (np. https://xxxxx.supabase.co)</li>
                  <li><strong>anon/public key</strong> (zaczyna się od eyJ...)</li>
                </ul>
              </li>
            </ol>
            <div className="bg-yellow-50 border border-yellow-200 rounded p-4">
              <p className="text-yellow-900"><strong>⚠️ Ważne:</strong> Klucze skopiuj dokładnie, ze spacjami</p>
            </div>
          </section>

          {/* Krok 2 */}
          <section className="mb-8 pb-8 border-b">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">Krok 2️⃣: Wstaw klucze do .env.local</h2>
            <p className="text-gray-700 mb-4">Otwórz plik <code className="bg-gray-200 px-2 py-1 rounded">.env.local</code> w edytorze i zastąp:</p>
            <div className="bg-gray-900 text-green-400 p-4 rounded font-mono text-sm mb-4 overflow-x-auto">
              <pre>{`# Zamieniaj placeholder'i na twoje prawdziwe klucze:
NEXT_PUBLIC_SUPABASE_URL=https://twój-projekt.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`}</pre>
            </div>
            <p className="text-gray-700"><strong>Gdzie znaleźć klucze:</strong> Supabase Dashboard → Settings → API</p>
          </section>

          {/* Krok 3 */}
          <section className="mb-8 pb-8 border-b">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">Krok 3️⃣: Uruchom SQL script</h2>
            <p className="text-gray-700 mb-4">W Supabase Dashboard:</p>
            <ol className="list-decimal pl-5 space-y-2 text-gray-700 mb-4">
              <li>Przejdź do: <strong>SQL Editor</strong></li>
              <li>Kliknij: <strong>New Query</strong></li>
              <li>Skopiuj i wklej poniższy kod:</li>
            </ol>
            <div className="bg-gray-900 text-green-400 p-4 rounded font-mono text-sm mb-4 overflow-x-auto">
              <pre className="text-xs">{`-- Utwórz tabelę dla profili użytkowników
create table if not exists public.profiles (
  id uuid references auth.users primary key,
  username text unique,
  full_name text,
  avatar_url text,
  bio text,
  created_at timestamp with time zone default now(),
  updated_at timestamp with time zone default now()
);

-- Utwórz tabelę dla projektów
create table if not exists public.projects (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references public.profiles(id) on delete cascade,
  title text not null,
  description text,
  status text default 'active',
  created_at timestamp with time zone default now(),
  updated_at timestamp with time zone default now()
);

-- Włącz Row Level Security
alter table public.profiles enable row level security;
alter table public.projects enable row level security;

-- Polityka RLS dla profiles
create policy "Users can view own profile"
on public.profiles for select
using (auth.uid() = id);

create policy "Users can update own profile"
on public.profiles for update
using (auth.uid() = id);

-- Polityka RLS dla projects
create policy "Users can view own projects"
on public.projects for select
using (auth.uid() = user_id);

create policy "Users can create projects"
on public.projects for insert
with check (auth.uid() = user_id);

create policy "Users can update own projects"
on public.projects for update
using (auth.uid() = user_id);`}</pre>
            </div>
            <p className="text-gray-700">Kliknij: <strong>Run</strong></p>
          </section>

          {/* Krok 4 */}
          <section className="mb-8">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">Krok 4️⃣: Zrestartuj serwer</h2>
            <p className="text-gray-700 mb-4">W terminalu:</p>
            <div className="bg-gray-900 text-green-400 p-4 rounded font-mono text-sm mb-4">
              <pre>{`Ctrl + C  (zatrzymaj serwer)
npm run dev  (uruchom ponownie)`}</pre>
            </div>
          </section>

          {/* Test */}
          <section className="bg-blue-50 border border-blue-200 rounded p-6 mb-8">
            <h2 className="text-2xl font-bold text-blue-900 mb-4">✅ Testowanie połączenia</h2>
            <p className="text-blue-900 mb-4">Jeśli wszystko jest gotowe, otwórz stronę testową:</p>
            <Link
              href="/test-connection"
              className="inline-block px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition font-bold"
            >
              Otwórz test połączenia →
            </Link>
          </section>

          {/* Troubleshooting */}
          <section className="bg-red-50 border border-red-200 rounded p-6">
            <h2 className="text-2xl font-bold text-red-900 mb-4">🆘 Troubleshooting</h2>
            <div className="space-y-4 text-red-900">
              <div>
                <strong>Problem:</strong> "Missing Supabase environment variables"
                <p className="text-sm mt-1">→ Sprawdź czy klucze są w .env.local i serwer został zrestartowany</p>
              </div>
              <div>
                <strong>Problem:</strong> "no rows returned"
                <p className="text-sm mt-1">→ Tabela "profiles" nie istnieje - uruchom SQL script w Supabase</p>
              </div>
              <div>
                <strong>Problem:</strong> "Row Level Security" blokuje zapytania
                <p className="text-sm mt-1">→ Sprawdź polityki RLS - mogą być za restrykcyjne</p>
              </div>
            </div>
          </section>
        </div>
      </div>
    </main>
  );
}
