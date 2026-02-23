/**
 * Supabase Client (Client-Side)
 *
 * Klient do użytku w komponentach React i client-side kod.
 * Używa publicznego klucza anon (NEXT_PUBLIC_SUPABASE_ANON_KEY).
 *
 * Środowisko: Browser
 * Bezpieczeństwo: Row Level Security (RLS) - obowiązkowe w produkcji
 *
 * Zasilł na podstawie:
 * - NEXT_PUBLIC_SUPABASE_URL
 * - NEXT_PUBLIC_SUPABASE_ANON_KEY
 */

// ...existing code...

import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL as string;
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY as string;

if (!supabaseUrl) {
  throw new Error(
    'Missing NEXT_PUBLIC_SUPABASE_URL. Check your .env.local file.'
  );
}

if (!supabaseAnonKey) {
  throw new Error(
    'Missing NEXT_PUBLIC_SUPABASE_ANON_KEY. Check your .env.local file.'
  );
}

export const supabase = createClient(supabaseUrl, supabaseAnonKey);
