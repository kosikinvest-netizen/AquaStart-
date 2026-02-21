/**
 * Database Types
 * Wygeneruj automatycznie typy z Supabase używając:
 * npx supabase gen types typescript --project-id your-project-ref > src/types/database.types.ts
 */

export type Json =
  | string
  | number
  | boolean
  | null
  | { [key: string]: Json | undefined }
  | Json[];

export interface Database {
  public: {
    Tables: {
      // Dodaj swoje tabele tutaj
      // Przykład:
      // users: {
      //   Row: {
      //     id: string;
      //     email: string;
      //     created_at: string;
      //   };
      //   Insert: {
      //     id?: string;
      //     email: string;
      //     created_at?: string;
      //   };
      //   Update: {
      //     id?: string;
      //     email?: string;
      //     created_at?: string;
      //   };
      // };
    };
    Views: {
      // Dodaj swoje views tutaj
    };
    Functions: {
      // Dodaj swoje funkcje tutaj
    };
    Enums: {
      // Dodaj swoje enumy tutaj
    };
  };
}
