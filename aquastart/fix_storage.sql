-- ============================================================================
-- SUPABASE STORAGE CONFIGURATION - FIX VERSION
-- Usuwa stare polityki i tworzy nowe
-- ============================================================================

-- 1. Utwórz bucket publications (jeśli nie istnieje)
INSERT INTO storage.buckets (id, name, public) 
VALUES ('publications', 'publications', true) 
ON CONFLICT (id) DO NOTHING;

-- 2. USUŃ stare polityki (jeśli istnieją)
DROP POLICY IF EXISTS "Publiczna opcja pobierania" ON storage.objects;
DROP POLICY IF EXISTS "Pozwól na wgrywanie" ON storage.objects;
DROP POLICY IF EXISTS "Pozwól na usuwanie" ON storage.objects;

-- 3. UTWÓRZ nowe polityki
-- Pozwala każdemu na pobieranie plików z bucketu publications
CREATE POLICY "Publiczna opcja pobierania" 
ON storage.objects FOR SELECT 
USING (bucket_id = 'publications');

-- Pozwala na wgrywanie plików do bucketu publications
CREATE POLICY "Pozwól na wgrywanie" 
ON storage.objects FOR INSERT 
WITH CHECK (bucket_id = 'publications');

-- Pozwala na usuwanie plików
CREATE POLICY "Pozwól na usuwanie" 
ON storage.objects FOR DELETE 
USING (bucket_id = 'publications');

-- ============================================================================
-- SUCCESS MESSAGE
-- ============================================================================
SELECT 
  'Storage configuration completed!' as status,
  'Bucket: publications' as bucket,
  'RLS Policies: 3 (SELECT, INSERT, DELETE)' as policies,
  'Status: Ready for PDF uploads' as ready;
