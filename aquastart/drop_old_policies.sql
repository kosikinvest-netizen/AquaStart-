-- Drop old policies if they exist (uncomment if needed)
-- DROP POLICY IF EXISTS "Publiczna opcja pobierania" ON public.objects;
-- DROP POLICY IF EXISTS "Użytkownicy mogą przesyłać pliki" ON public.objects;
-- DROP POLICY IF EXISTS "Użytkownicy mogą usuwać swoje pliki" ON public.objects;

-- Clean version for fresh start:
DROP POLICY IF EXISTS "Publiczna opcja pobierania" ON public.objects;
DROP POLICY IF EXISTS "Allow public select" ON public.objects;
DROP POLICY IF EXISTS "Users can read own PDFs" ON public.pdf_publications;
DROP POLICY IF EXISTS "Users can insert own PDFs" ON public.pdf_publications;
DROP POLICY IF EXISTS "Users can update own PDFs" ON public.pdf_publications;
DROP POLICY IF EXISTS "Users can delete own PDFs" ON public.pdf_publications;
