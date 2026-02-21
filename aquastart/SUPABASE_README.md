# Konfiguracja Supabase w AquaStart

## 🚀 Setup

### 1. Uzyskaj dane do połączenia

1. Zaloguj się do [Supabase Dashboard](https://app.supabase.com)
2. Wybierz swój projekt lub utwórz nowy
3. Przejdź do **Settings** → **API**
4. Skopiuj:
   - **Project URL** (jako `NEXT_PUBLIC_SUPABASE_URL`)
   - **anon/public key** (jako `NEXT_PUBLIC_SUPABASE_ANON_KEY`)
   - **(Opcjonalnie)** **service_role key** (jako `SUPABASE_SERVICE_ROLE_KEY`)

### 2. Zaktualizuj plik `.env.local`

Otwórz plik `.env.local` i zaktualizuj wartości:

```env
NEXT_PUBLIC_SUPABASE_URL=https://twój-projekt-ref.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=twój-klucz-anon
SUPABASE_SERVICE_ROLE_KEY=twój-klucz-service-role  # Tylko dla operacji server-side
```

⚠️ **WAŻNE**: 
- `NEXT_PUBLIC_*` - zmienne widoczne w przeglądarce
- `SUPABASE_SERVICE_ROLE_KEY` - używaj TYLKO po stronie serwera (API routes, Server Components)

### 3. Restart serwera dev

Po zmianie `.env.local`:

```bash
npm run dev
```

## 📁 Struktura plików

```
src/
├── lib/
│   ├── supabase.ts              # Klient dla client-side
│   ├── supabase-server.ts       # Klient dla server-side
│   └── supabase-examples.ts     # Przykłady użycia
├── types/
│   └── database.types.ts        # Typy bazy danych
```

## 🔧 Użycie

### Client Side (Components)

```typescript
import { supabase } from '@/lib/supabase';

export default function MyComponent() {
  const fetchData = async () => {
    const { data, error } = await supabase
      .from('your_table')
      .select('*');
    
    if (error) console.error(error);
    return data;
  };
}
```

### Server Side (API Routes)

```typescript
// app/api/data/route.ts
import { supabaseServer } from '@/lib/supabase-server';

export async function GET() {
  const { data, error } = await supabaseServer
    .from('your_table')
    .select('*');
  
  if (error) return Response.json({ error }, { status: 500 });
  return Response.json(data);
}
```

### Server Components (Next.js 14)

```typescript
import { supabase } from '@/lib/supabase';

export default async function ServerComponent() {
  const { data } = await supabase.from('your_table').select('*');
  
  return <div>{/* render data */}</div>;
}
```

## 🎯 Typowanie

### Generowanie typów z bazy danych

Zainstaluj Supabase CLI:

```bash
npm install -g supabase
```

Wygeneruj typy:

```bash
supabase gen types typescript --project-id twój-projekt-ref > src/types/database.types.ts
```

Użyj typów:

```typescript
import { Database } from '@/types/database.types';
import { createClient } from '@supabase/supabase-js';

export const supabase = createClient<Database>(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);
```

## 📚 Podstawowe operacje

### CRUD Operations

```typescript
// Create
const { data, error } = await supabase
  .from('table')
  .insert([{ column: 'value' }])
  .select();

// Read
const { data, error } = await supabase
  .from('table')
  .select('*')
  .eq('id', 1);

// Update
const { data, error } = await supabase
  .from('table')
  .update({ column: 'new value' })
  .eq('id', 1);

// Delete
const { error } = await supabase
  .from('table')
  .delete()
  .eq('id', 1);
```

### Autentykacja

```typescript
// Sign Up
const { data, error } = await supabase.auth.signUp({
  email: 'user@example.com',
  password: 'password123'
});

// Sign In
const { data, error } = await supabase.auth.signInWithPassword({
  email: 'user@example.com',
  password: 'password123'
});

// Sign Out
await supabase.auth.signOut();

// Get User
const { data: { user } } = await supabase.auth.getUser();
```

### Storage (pliki)

```typescript
// Upload
const { data, error } = await supabase.storage
  .from('bucket-name')
  .upload('path/to/file.png', file);

// Download URL
const { data } = supabase.storage
  .from('bucket-name')
  .getPublicUrl('path/to/file.png');
```

### Real-time

```typescript
const channel = supabase
  .channel('table-changes')
  .on('postgres_changes', 
    { event: '*', schema: 'public', table: 'your_table' },
    (payload) => {
      console.log('Change received!', payload);
    }
  )
  .subscribe();

// Cleanup
supabase.removeChannel(channel);
```

## 🔐 Bezpieczeństwo

### Row Level Security (RLS)

**ZAWSZE włączaj RLS** na swoich tabelach w Supabase:

```sql
-- Włącz RLS
ALTER TABLE your_table ENABLE ROW LEVEL SECURITY;

-- Przykładowa polityka - użytkownicy mogą czytać tylko swoje dane
CREATE POLICY "Users can view own data"
ON your_table FOR SELECT
USING (auth.uid() = user_id);

-- Przykładowa polityka - użytkownicy mogą tworzyć dane
CREATE POLICY "Users can insert own data"
ON your_table FOR INSERT
WITH CHECK (auth.uid() = user_id);
```

### Bezpieczeństwo kluczy

- ✅ `NEXT_PUBLIC_SUPABASE_ANON_KEY` - bezpieczny w przeglądarce (chroniony przez RLS)
- ❌ `SUPABASE_SERVICE_ROLE_KEY` - NIE ujawniaj w kodzie client-side!

## 📖 Dodatkowe zasoby

- [Dokumentacja Supabase](https://supabase.com/docs)
- [Supabase JavaScript Client](https://supabase.com/docs/reference/javascript)
- [Next.js + Supabase Guide](https://supabase.com/docs/guides/getting-started/quickstarts/nextjs)
- [Przykłady użycia](./src/lib/supabase-examples.ts)

## 🆘 Troubleshooting

### Problem: "Missing Supabase environment variables"

**Rozwiązanie**: Upewnij się że `.env.local` zawiera poprawne zmienne i zrestartuj serwer dev.

### Problem: "Row Level Security" blokuje zapytania

**Rozwiązanie**: Skonfiguruj polityki RLS w Supabase Dashboard lub tymczasowo wyłącz RLS dla testów.

### Problem: Typy nie są aktualne

**Rozwiązanie**: Wygeneruj ponownie typy używając Supabase CLI:
```bash
supabase gen types typescript --project-id twój-projekt-ref > src/types/database.types.ts
```
