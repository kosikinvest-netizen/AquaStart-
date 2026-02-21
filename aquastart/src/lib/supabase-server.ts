import { createClient } from '@supabase/supabase-js';

/**
 * Klient Supabase po stronie serwera z Service Role Key
 * UWAGA: Używaj tylko w API routes lub Server Components!
 * Ten klient ma pełne uprawnienia i pomija Row Level Security (RLS)
 */

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const supabaseServiceRoleKey = process.env.SUPABASE_SERVICE_ROLE_KEY!;

if (!supabaseUrl || !supabaseServiceRoleKey) {
  throw new Error('Missing Supabase server environment variables');
}

export const supabaseServer = createClient(supabaseUrl, supabaseServiceRoleKey, {
  auth: {
    autoRefreshToken: false,
    persistSession: false,
  },
});
