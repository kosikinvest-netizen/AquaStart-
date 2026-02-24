-- AquaStart - Supabase RLS Configuration
-- Run this in Supabase SQL Editor

-- ============================================================================
-- 1. CREATE TABLES (if not exist)
-- ============================================================================

-- Users table (extends auth.users)
CREATE TABLE IF NOT EXISTS public.users (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  email TEXT UNIQUE NOT NULL,
  full_name TEXT,
  avatar_url TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Aquarium configurations
CREATE TABLE IF NOT EXISTS public.aquariums (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  type TEXT NOT NULL, -- 'freshwater', 'saltwater', 'brackish'
  volume_liters INTEGER NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Water parameters
CREATE TABLE IF NOT EXISTS public.water_parameters (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  aquarium_id UUID NOT NULL REFERENCES public.aquariums(id) ON DELETE CASCADE,
  ph DECIMAL(3,1),
  temperature DECIMAL(4,2),
  ammonia DECIMAL(5,3),
  nitrite DECIMAL(5,3),
  nitrate DECIMAL(5,2),
  recorded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Generated reports
CREATE TABLE IF NOT EXISTS public.reports (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
  aquarium_id UUID REFERENCES public.aquariums(id) ON DELETE SET NULL,
  title TEXT NOT NULL,
  content TEXT,
  pdf_path TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================================================
-- 2. ENABLE ROW LEVEL SECURITY
-- ============================================================================

ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.aquariums ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.water_parameters ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.reports ENABLE ROW LEVEL SECURITY;

-- ============================================================================
-- 3. CREATE RLS POLICIES
-- ============================================================================

-- Users: Can only read/update their own profile
CREATE POLICY "Users can read own profile"
  ON public.users FOR SELECT
  USING (auth.uid() = id);

CREATE POLICY "Users can update own profile"
  ON public.users FOR UPDATE
  USING (auth.uid() = id);

-- Aquariums: Can only access own aquariums
CREATE POLICY "Users can read own aquariums"
  ON public.aquariums FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own aquariums"
  ON public.aquariums FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own aquariums"
  ON public.aquariums FOR UPDATE
  USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own aquariums"
  ON public.aquariums FOR DELETE
  USING (auth.uid() = user_id);

-- Water Parameters: Can only access parameters from own aquariums
CREATE POLICY "Users can read own aquarium parameters"
  ON public.water_parameters FOR SELECT
  USING (
    aquarium_id IN (
      SELECT id FROM public.aquariums 
      WHERE user_id = auth.uid()
    )
  );

CREATE POLICY "Users can insert parameters to own aquariums"
  ON public.water_parameters FOR INSERT
  WITH CHECK (
    aquarium_id IN (
      SELECT id FROM public.aquariums 
      WHERE user_id = auth.uid()
    )
  );

-- Reports: Can only access own reports
CREATE POLICY "Users can read own reports"
  ON public.reports FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own reports"
  ON public.reports FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete own reports"
  ON public.reports FOR DELETE
  USING (auth.uid() = user_id);

-- ============================================================================
-- 4. CREATE INDEXES (for performance)
-- ============================================================================

CREATE INDEX IF NOT EXISTS idx_aquariums_user_id ON public.aquariums(user_id);
CREATE INDEX IF NOT EXISTS idx_water_parameters_aquarium_id ON public.water_parameters(aquarium_id);
CREATE INDEX IF NOT EXISTS idx_water_parameters_recorded_at ON public.water_parameters(recorded_at DESC);
CREATE INDEX IF NOT EXISTS idx_reports_user_id ON public.reports(user_id);

-- ============================================================================
-- 5. CREATE FUNCTIONS (for triggers)
-- ============================================================================

-- Update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create triggers
CREATE TRIGGER update_users_updated_at
  BEFORE UPDATE ON public.users
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_aquariums_updated_at
  BEFORE UPDATE ON public.aquariums
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- 6. GRANT PERMISSIONS
-- ============================================================================

-- ============================================================================
-- SUPABASE STORAGE CONFIGURATION - SAFE VERSION
-- ============================================================================

-- Tworzy publiczny bucket o nazwie 'publications'
INSERT INTO storage.buckets (id, name, public) 
VALUES ('publications', 'publications', true) 
ON CONFLICT (id) DO NOTHING;

-- Usuń stare polityki jeśli istnieją (opcjonalnie)
DROP POLICY IF EXISTS "Publiczna opcja pobierania" ON storage.objects;
DROP POLICY IF EXISTS "Pozwól na wgrywanie" ON storage.objects;

-- Pozwala każdemu na pobieranie plików (z IF NOT EXISTS)
CREATE POLICY IF NOT EXISTS "Publiczna opcja pobierania" 
ON storage.objects FOR SELECT 
USING (bucket_id = 'publications');

-- Pozwala skryptowi na wgrywanie plików (z IF NOT EXISTS)
CREATE POLICY IF NOT EXISTS "Pozwól na wgrywanie" 
ON storage.objects FOR INSERT 
WITH CHECK (bucket_id = 'publications');

-- Pozwala na usuwanie własnych plików
CREATE POLICY IF NOT EXISTS "Pozwól na usuwanie" 
ON storage.objects FOR DELETE 
USING (bucket_id = 'publications');

SELECT 'Storage configuration complete!' as status;
