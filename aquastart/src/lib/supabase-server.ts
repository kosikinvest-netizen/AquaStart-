/**
 * Supabase Client (Server-Side)
 *
 * Klient do używania tylko w API routes i Server Components (Next.js 14+).
 * Używa Service Role Key - pełne uprawnienia, omija Row Level Security!
 *
 * UWAGA: Nigdy nie ujawniaj Service Role Key w public codzie lub przeglądarce.
 * Używaj TYLKO po stronie serwera (API routes, getServerSideProps, itp.)
 *
 * Środowisko: Next.js Server
 * Bezpieczeństwo: Brak RLS - potrzebna własna walidacja dostępu
 *
 * Zasilany na podstawie:
 * - NEXT_PUBLIC_SUPABASE_URL
 * - SUPABASE_SERVICE_ROLE_KEY (secret, nie public!)
 */

import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
const supabaseServiceRoleKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

if (!supabaseUrl) {
  throw new Error(
    'Missing NEXT_PUBLIC_SUPABASE_URL. Check your .env.local file.'
  );
}

if (!supabaseServiceRoleKey) {
  throw new Error(
    'Missing SUPABASE_SERVICE_ROLE_KEY. Check your .env.local file. ' +
    'This is a SECRET - keep it safe!'
  );
}

export const supabaseServer = createClient(supabaseUrl, supabaseServiceRoleKey, {
  auth: {
    autoRefreshToken: false,
    persistSession: false,
  },
});
