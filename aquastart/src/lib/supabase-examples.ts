/**
 * Przykłady użycia Supabase w projekcie AquaStart
 */

import { supabase } from '@/lib/supabase';
import { supabaseServer } from '@/lib/supabase-server';

// ============================================
// PRZYKŁAD 1: Pobieranie danych (Client Side)
// ============================================

export async function fetchDataExample() {
  const { data, error } = await supabase
    .from('your_table')
    .select('*');
  
  if (error) {
    console.error('Error fetching data:', error);
    return null;
  }
  
  return data;
}

// ============================================
// PRZYKŁAD 2: Dodawanie danych
// ============================================

export async function insertDataExample(newData: any) {
  const { data, error } = await supabase
    .from('your_table')
    .insert([newData])
    .select();
  
  if (error) {
    console.error('Error inserting data:', error);
    return null;
  }
  
  return data;
}

// ============================================
// PRZYKŁAD 3: Aktualizacja danych
// ============================================

export async function updateDataExample(id: string, updates: any) {
  const { data, error } = await supabase
    .from('your_table')
    .update(updates)
    .eq('id', id)
    .select();
  
  if (error) {
    console.error('Error updating data:', error);
    return null;
  }
  
  return data;
}

// ============================================
// PRZYKŁAD 4: Usuwanie danych
// ============================================

export async function deleteDataExample(id: string) {
  const { error } = await supabase
    .from('your_table')
    .delete()
    .eq('id', id);
  
  if (error) {
    console.error('Error deleting data:', error);
    return false;
  }
  
  return true;
}

// ============================================
// PRZYKŁAD 5: Autentykacja - Rejestracja
// ============================================

export async function signUpExample(email: string, password: string) {
  const { data, error } = await supabase.auth.signUp({
    email,
    password,
  });
  
  if (error) {
    console.error('Error signing up:', error);
    return null;
  }
  
  return data;
}

// ============================================
// PRZYKŁAD 6: Autentykacja - Logowanie
// ============================================

export async function signInExample(email: string, password: string) {
  const { data, error } = await supabase.auth.signInWithPassword({
    email,
    password,
  });
  
  if (error) {
    console.error('Error signing in:', error);
    return null;
  }
  
  return data;
}

// ============================================
// PRZYKŁAD 7: Autentykacja - Wylogowanie
// ============================================

export async function signOutExample() {
  const { error } = await supabase.auth.signOut();
  
  if (error) {
    console.error('Error signing out:', error);
    return false;
  }
  
  return true;
}

// ============================================
// PRZYKŁAD 8: Pobieranie obecnego użytkownika
// ============================================

export async function getCurrentUserExample() {
  const { data: { user }, error } = await supabase.auth.getUser();
  
  if (error) {
    console.error('Error getting user:', error);
    return null;
  }
  
  return user;
}

// ============================================
// PRZYKŁAD 9: Real-time subscription
// ============================================

export function subscribeToChangesExample(callback: (payload: any) => void) {
  const channel = supabase
    .channel('table-changes')
    .on(
      'postgres_changes',
      {
        event: '*',
        schema: 'public',
        table: 'your_table'
      },
      callback
    )
    .subscribe();
  
  // Zwróć funkcję do cleanup
  return () => {
    supabase.removeChannel(channel);
  };
}

// ============================================
// PRZYKŁAD 10: Upload pliku
// ============================================

export async function uploadFileExample(file: File, bucket: string, path: string) {
  const { data, error } = await supabase.storage
    .from(bucket)
    .upload(path, file);
  
  if (error) {
    console.error('Error uploading file:', error);
    return null;
  }
  
  return data;
}

// ============================================
// PRZYKŁAD 11: Pobieranie URL pliku
// ============================================

export function getPublicUrlExample(bucket: string, path: string) {
  const { data } = supabase.storage
    .from(bucket)
    .getPublicUrl(path);
  
  return data.publicUrl;
}

// ============================================
// PRZYKŁAD 12: Server-side query (API Route)
// ============================================

export async function serverSideQueryExample() {
  // Używaj tego tylko w API routes lub Server Components
  const { data, error } = await supabaseServer
    .from('your_table')
    .select('*');
  
  if (error) {
    console.error('Error fetching data:', error);
    return null;
  }
  
  return data;
}

// ============================================
// PRZYKŁAD 13: Filtrowanie i sortowanie
// ============================================

export async function advancedQueryExample() {
  const { data, error } = await supabase
    .from('your_table')
    .select('*')
    .eq('status', 'active')
    .gte('created_at', '2024-01-01')
    .order('created_at', { ascending: false })
    .limit(10);
  
  if (error) {
    console.error('Error fetching data:', error);
    return null;
  }
  
  return data;
}

// ============================================
// PRZYKŁAD 14: Join z innymi tabelami
// ============================================

export async function joinQueryExample() {
  const { data, error } = await supabase
    .from('posts')
    .select(`
      *,
      author:users(id, name, email),
      comments(*)
    `);
  
  if (error) {
    console.error('Error fetching data:', error);
    return null;
  }
  
  return data;
}
