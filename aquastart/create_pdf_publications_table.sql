-- ============================================================================
-- AquaStart: PDF Publications Table
-- Tabela do przechowywania metadanych plików PDF
-- ============================================================================

-- Create pdf_publications table (aplikacyjna, nie Storage)
CREATE TABLE IF NOT EXISTS public.pdf_publications (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  type TEXT NOT NULL,
  file_url TEXT NOT NULL,
  file_size INTEGER,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable RLS on our table
ALTER TABLE public.pdf_publications ENABLE ROW LEVEL SECURITY;

-- Policy 1: Users can read own PDFs + public PDFs
CREATE POLICY IF NOT EXISTS "pdf_read_own_or_public"
  ON public.pdf_publications
  FOR SELECT
  USING (auth.uid() = user_id OR user_id IS NULL);

-- Policy 2: Users can insert their own PDFs
CREATE POLICY IF NOT EXISTS "pdf_insert_own"
  ON public.pdf_publications
  FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- Policy 3: Users can update their own PDFs
CREATE POLICY IF NOT EXISTS "pdf_update_own"
  ON public.pdf_publications
  FOR UPDATE
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

-- Policy 4: Users can delete their own PDFs
CREATE POLICY IF NOT EXISTS "pdf_delete_own"
  ON public.pdf_publications
  FOR DELETE
  USING (auth.uid() = user_id);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_pdf_publications_user_id ON public.pdf_publications(user_id);
CREATE INDEX IF NOT EXISTS idx_pdf_publications_created_at ON public.pdf_publications(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_pdf_publications_file_url ON public.pdf_publications(file_url);

-- Auto-update timestamp function
CREATE OR REPLACE FUNCTION update_pdf_publications_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger for auto-update
DROP TRIGGER IF EXISTS pdf_publications_updated_at_trigger ON public.pdf_publications;
CREATE TRIGGER pdf_publications_updated_at_trigger
  BEFORE UPDATE ON public.pdf_publications
  FOR EACH ROW
  EXECUTE FUNCTION update_pdf_publications_updated_at();

-- Grant permissions
GRANT SELECT, INSERT, UPDATE, DELETE ON public.pdf_publications TO authenticated;
GRANT USAGE ON SEQUENCE public.pdf_publications_id_seq TO authenticated;

-- Signal success
SELECT 'PDF Publications table created successfully!' as status;
