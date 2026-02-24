-- Create pdf_publications table
CREATE TABLE IF NOT EXISTS public.pdf_publications (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES public.users(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  type TEXT NOT NULL,
  file_url TEXT NOT NULL,
  file_size INTEGER,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE public.pdf_publications ENABLE ROW LEVEL SECURITY;

-- RLS Policies
CREATE POLICY "Users can read own PDFs"
  ON public.pdf_publications FOR SELECT
  USING (auth.uid() = user_id OR user_id IS NULL);

CREATE POLICY "Users can insert own PDFs"
  ON public.pdf_publications FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own PDFs"
  ON public.pdf_publications FOR UPDATE
  USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own PDFs"
  ON public.pdf_publications FOR DELETE
  USING (auth.uid() = user_id);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_pdf_publications_user_id ON public.pdf_publications(user_id);
CREATE INDEX IF NOT EXISTS idx_pdf_publications_created_at ON public.pdf_publications(created_at DESC);

-- Create trigger
CREATE TRIGGER update_pdf_publications_updated_at
  BEFORE UPDATE ON public.pdf_publications
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();
