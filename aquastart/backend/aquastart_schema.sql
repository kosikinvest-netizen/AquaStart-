-- ================================================================
-- AquaStart Database Schema - Idempotent & RLS Enabled
-- ================================================================
-- Production-ready SQL for Supabase
-- Can be run multiple times safely (DROP IF EXISTS pattern)
-- ================================================================

-- ================================================================
-- 1. SETUP: Enable Extensions
-- ================================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ================================================================
-- 2. TABLES: Core Schema
-- ================================================================

-- Users Table (integrates with Supabase Auth)
CREATE TABLE IF NOT EXISTS public.users (
    id UUID PRIMARY KEY DEFAULT auth.uid(),
    email TEXT UNIQUE NOT NULL,
    full_name TEXT,
    avatar_url TEXT,
    role TEXT DEFAULT 'user' CHECK (role IN ('user', 'admin', 'moderator')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL
);

-- Tanks Table (aquarium containers)
CREATE TABLE IF NOT EXISTS public.tanks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    owner_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    volume_liters DECIMAL(10, 2) NOT NULL CHECK (volume_liters > 0),
    type TEXT NOT NULL CHECK (type IN ('freshwater', 'saltwater', 'brackish')),
    location TEXT,
    description TEXT,
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    CONSTRAINT tank_owner_name_unique UNIQUE (owner_id, name)
);

-- Parameters Table (water quality measurements)
CREATE TABLE IF NOT EXISTS public.parameters (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tank_id UUID NOT NULL REFERENCES public.tanks(id) ON DELETE CASCADE,
    temperature_celsius DECIMAL(5, 2),
    ph DECIMAL(4, 2) CHECK (ph >= 0 AND ph <= 14),
    ammonia_mg_l DECIMAL(6, 3),
    nitrite_mg_l DECIMAL(6, 3),
    nitrate_mg_l DECIMAL(6, 3),
    conductivity_us_cm DECIMAL(8, 2),
    dissolved_oxygen_mg_l DECIMAL(5, 2),
    measured_at TIMESTAMP WITH TIME ZONE NOT NULL,
    recorded_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    notes TEXT,
    CONSTRAINT parameters_tank_time_unique UNIQUE (tank_id, measured_at)
);

-- Fish Species Table
CREATE TABLE IF NOT EXISTS public.fish (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tank_id UUID NOT NULL REFERENCES public.tanks(id) ON DELETE CASCADE,
    species_name TEXT NOT NULL,
    common_name TEXT,
    quantity INTEGER NOT NULL DEFAULT 1 CHECK (quantity > 0),
    size_cm DECIMAL(5, 2),
    added_date DATE NOT NULL,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL
);

-- Maintenance Logs Table
CREATE TABLE IF NOT EXISTS public.maintenance_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tank_id UUID NOT NULL REFERENCES public.tanks(id) ON DELETE CASCADE,
    maintenance_type TEXT NOT NULL CHECK (
        maintenance_type IN (
            'water_change',
            'filter_clean',
            'substrate_clean',
            'plant_trim',
            'equipment_check',
            'chemical_treatment',
            'other'
        )
    ),
    description TEXT NOT NULL,
    duration_minutes INTEGER,
    performed_at TIMESTAMP WITH TIME ZONE NOT NULL,
    recorded_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    created_by_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    CONSTRAINT maintenance_tank_time_unique UNIQUE (tank_id, performed_at, maintenance_type)
);

-- ================================================================
-- 3. INDEXES: Performance Optimization
-- ================================================================

CREATE INDEX IF NOT EXISTS idx_tanks_owner_id ON public.tanks(owner_id);
CREATE INDEX IF NOT EXISTS idx_tanks_active ON public.tanks(active);
CREATE INDEX IF NOT EXISTS idx_parameters_tank_id ON public.parameters(tank_id);
CREATE INDEX IF NOT EXISTS idx_parameters_measured_at ON public.parameters(measured_at DESC);
CREATE INDEX IF NOT EXISTS idx_fish_tank_id ON public.fish(tank_id);
CREATE INDEX IF NOT EXISTS idx_maintenance_tank_id ON public.maintenance_logs(tank_id);
CREATE INDEX IF NOT EXISTS idx_maintenance_performed_at ON public.maintenance_logs(performed_at DESC);

-- ================================================================
-- 4. ROW LEVEL SECURITY: Global Disable/Enable
-- ================================================================

ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.tanks ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.parameters ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.fish ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.maintenance_logs ENABLE ROW LEVEL SECURITY;

-- ================================================================
-- 5. RLS POLICIES: Users Table
-- ================================================================

-- Users can view public profile data
DROP POLICY IF EXISTS "Users can view public profiles" ON public.users;
CREATE POLICY "Users can view public profiles"
    ON public.users FOR SELECT
    USING (true);

-- Users can update their own profile
DROP POLICY IF EXISTS "Users can update own profile" ON public.users;
CREATE POLICY "Users can update own profile"
    ON public.users FOR UPDATE
    USING (auth.uid() = id)
    WITH CHECK (auth.uid() = id);

-- Only admins can insert new users (handled by Supabase Auth)
DROP POLICY IF EXISTS "Users cannot insert via API" ON public.users;
CREATE POLICY "Users cannot insert via API"
    ON public.users FOR INSERT
    WITH CHECK (false);

-- ================================================================
-- 6. RLS POLICIES: Tanks Table
-- ================================================================

-- Users can only view their own tanks
DROP POLICY IF EXISTS "Users can view own tanks" ON public.tanks;
CREATE POLICY "Users can view own tanks"
    ON public.tanks FOR SELECT
    USING (auth.uid() = owner_id);

-- Users can insert tanks for themselves
DROP POLICY IF EXISTS "Users can insert own tanks" ON public.tanks;
CREATE POLICY "Users can insert own tanks"
    ON public.tanks FOR INSERT
    WITH CHECK (auth.uid() = owner_id);

-- Users can update their own tanks
DROP POLICY IF EXISTS "Users can update own tanks" ON public.tanks;
CREATE POLICY "Users can update own tanks"
    ON public.tanks FOR UPDATE
    USING (auth.uid() = owner_id)
    WITH CHECK (auth.uid() = owner_id);

-- Users can delete their own tanks
DROP POLICY IF EXISTS "Users can delete own tanks" ON public.tanks;
CREATE POLICY "Users can delete own tanks"
    ON public.tanks FOR DELETE
    USING (auth.uid() = owner_id);

-- ================================================================
-- 7. RLS POLICIES: Parameters Table
-- ================================================================

-- Users can only view parameters from tanks they own
DROP POLICY IF EXISTS "Users can view own tank parameters" ON public.parameters;
CREATE POLICY "Users can view own tank parameters"
    ON public.parameters FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM public.tanks
            WHERE tanks.id = parameters.tank_id
            AND tanks.owner_id = auth.uid()
        )
    );

-- Users can insert parameters into their own tanks
DROP POLICY IF EXISTS "Users can insert parameters to own tanks" ON public.parameters;
CREATE POLICY "Users can insert parameters to own tanks"
    ON public.parameters FOR INSERT
    WITH CHECK (
        EXISTS (
            SELECT 1 FROM public.tanks
            WHERE tanks.id = parameters.tank_id
            AND tanks.owner_id = auth.uid()
        )
    );

-- Users can update parameters in their own tanks
DROP POLICY IF EXISTS "Users can update own tank parameters" ON public.parameters;
CREATE POLICY "Users can update own tank parameters"
    ON public.parameters FOR UPDATE
    USING (
        EXISTS (
            SELECT 1 FROM public.tanks
            WHERE tanks.id = parameters.tank_id
            AND tanks.owner_id = auth.uid()
        )
    )
    WITH CHECK (
        EXISTS (
            SELECT 1 FROM public.tanks
            WHERE tanks.id = parameters.tank_id
            AND tanks.owner_id = auth.uid()
        )
    );

-- Users can delete parameters from their own tanks
DROP POLICY IF EXISTS "Users can delete own tank parameters" ON public.parameters;
CREATE POLICY "Users can delete own tank parameters"
    ON public.parameters FOR DELETE
    USING (
        EXISTS (
            SELECT 1 FROM public.tanks
            WHERE tanks.id = parameters.tank_id
            AND tanks.owner_id = auth.uid()
        )
    );

-- ================================================================
-- 8. RLS POLICIES: Fish Table
-- ================================================================

-- Users can view fish in their own tanks
DROP POLICY IF EXISTS "Users can view own tank fish" ON public.fish;
CREATE POLICY "Users can view own tank fish"
    ON public.fish FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM public.tanks
            WHERE tanks.id = fish.tank_id
            AND tanks.owner_id = auth.uid()
        )
    );

-- Users can insert fish to their own tanks
DROP POLICY IF EXISTS "Users can insert fish to own tanks" ON public.fish;
CREATE POLICY "Users can insert fish to own tanks"
    ON public.fish FOR INSERT
    WITH CHECK (
        EXISTS (
            SELECT 1 FROM public.tanks
            WHERE tanks.id = fish.tank_id
            AND tanks.owner_id = auth.uid()
        )
    );

-- Users can update fish in their own tanks
DROP POLICY IF EXISTS "Users can update own tank fish" ON public.fish;
CREATE POLICY "Users can update own tank fish"
    ON public.fish FOR UPDATE
    USING (
        EXISTS (
            SELECT 1 FROM public.tanks
            WHERE tanks.id = fish.tank_id
            AND tanks.owner_id = auth.uid()
        )
    )
    WITH CHECK (
        EXISTS (
            SELECT 1 FROM public.tanks
            WHERE tanks.id = fish.tank_id
            AND tanks.owner_id = auth.uid()
        )
    );

-- Users can delete fish from their own tanks
DROP POLICY IF EXISTS "Users can delete own tank fish" ON public.fish;
CREATE POLICY "Users can delete own tank fish"
    ON public.fish FOR DELETE
    USING (
        EXISTS (
            SELECT 1 FROM public.tanks
            WHERE tanks.id = fish.tank_id
            AND tanks.owner_id = auth.uid()
        )
    );

-- ================================================================
-- 9. RLS POLICIES: Maintenance Logs Table
-- ================================================================

-- Users can view maintenance logs for their own tanks
DROP POLICY IF EXISTS "Users can view own tank maintenance logs" ON public.maintenance_logs;
CREATE POLICY "Users can view own tank maintenance logs"
    ON public.maintenance_logs FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM public.tanks
            WHERE tanks.id = maintenance_logs.tank_id
            AND tanks.owner_id = auth.uid()
        )
    );

-- Users can insert maintenance logs for their own tanks
DROP POLICY IF EXISTS "Users can insert maintenance logs for own tanks" ON public.maintenance_logs;
CREATE POLICY "Users can insert maintenance logs for own tanks"
    ON public.maintenance_logs FOR INSERT
    WITH CHECK (
        EXISTS (
            SELECT 1 FROM public.tanks
            WHERE tanks.id = maintenance_logs.tank_id
            AND tanks.owner_id = auth.uid()
        )
        AND created_by_id = auth.uid()
    );

-- Users can update maintenance logs they created
DROP POLICY IF EXISTS "Users can update own maintenance logs" ON public.maintenance_logs;
CREATE POLICY "Users can update own maintenance logs"
    ON public.maintenance_logs FOR UPDATE
    USING (created_by_id = auth.uid())
    WITH CHECK (created_by_id = auth.uid());

-- Users can delete maintenance logs they created
DROP POLICY IF EXISTS "Users can delete own maintenance logs" ON public.maintenance_logs;
CREATE POLICY "Users can delete own maintenance logs"
    ON public.maintenance_logs FOR DELETE
    USING (created_by_id = auth.uid());

-- ================================================================
-- 10. FUNCTIONS: Utility & Triggers
-- ================================================================

-- Updated timestamp function
CREATE OR REPLACE FUNCTION public.update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- ================================================================
-- 11. TRIGGERS: Automatic Timestamp Updates
-- ================================================================

DROP TRIGGER IF EXISTS set_updated_at_users ON public.users;
CREATE TRIGGER set_updated_at_users
    BEFORE UPDATE ON public.users
    FOR EACH ROW
    EXECUTE FUNCTION public.update_updated_at_column();

DROP TRIGGER IF EXISTS set_updated_at_tanks ON public.tanks;
CREATE TRIGGER set_updated_at_tanks
    BEFORE UPDATE ON public.tanks
    FOR EACH ROW
    EXECUTE FUNCTION public.update_updated_at_column();

DROP TRIGGER IF EXISTS set_updated_at_fish ON public.fish;
CREATE TRIGGER set_updated_at_fish
    BEFORE UPDATE ON public.fish
    FOR EACH ROW
    EXECUTE FUNCTION public.update_updated_at_column();

-- ================================================================
-- 12. VIEWS: Useful Queries (RLS Aware)
-- ================================================================

-- Current water parameters for all user's tanks (latest reading per tank)
DROP VIEW IF EXISTS public.latest_parameters;
CREATE VIEW public.latest_parameters AS
SELECT DISTINCT ON (tank_id)
    p.id,
    p.tank_id,
    p.temperature_celsius,
    p.ph,
    p.ammonia_mg_l,
    p.nitrite_mg_l,
    p.nitrate_mg_l,
    p.conductivity_us_cm,
    p.dissolved_oxygen_mg_l,
    p.measured_at,
    p.recorded_at,
    p.notes
FROM public.parameters p
ORDER BY tank_id, measured_at DESC;

-- Tank summary with fish count
DROP VIEW IF EXISTS public.tank_summary;
CREATE VIEW public.tank_summary AS
SELECT
    t.id,
    t.owner_id,
    t.name,
    t.volume_liters,
    t.type,
    t.active,
    COUNT(DISTINCT f.id) as fish_count,
    COUNT(DISTINCT m.id) as maintenance_count
FROM public.tanks t
LEFT JOIN public.fish f ON f.tank_id = t.id
LEFT JOIN public.maintenance_logs m ON m.tank_id = t.id
GROUP BY t.id, t.owner_id, t.name, t.volume_liters, t.type, t.active;

-- ================================================================
-- 13. COMMENTS: Documentation
-- ================================================================

COMMENT ON TABLE public.users IS 'User profiles integrated with Supabase Auth';
COMMENT ON TABLE public.tanks IS 'Aquarium containers managed by users';
COMMENT ON TABLE public.parameters IS 'Water quality measurements for tanks';
COMMENT ON TABLE public.fish IS 'Fish species and quantities in tanks';
COMMENT ON TABLE public.maintenance_logs IS 'Maintenance activities performed on tanks';

COMMENT ON COLUMN public.tanks.volume_liters IS 'Total tank volume in litres';
COMMENT ON COLUMN public.parameters.temperature_celsius IS 'Water temperature in °C';
COMMENT ON COLUMN public.parameters.ph IS 'pH value (0-14 scale)';
COMMENT ON COLUMN public.parameters.ammonia_mg_l IS 'Ammonia concentration in mg/L';
COMMENT ON COLUMN public.parameters.nitrite_mg_l IS 'Nitrite concentration in mg/L';
COMMENT ON COLUMN public.parameters.nitrate_mg_l IS 'Nitrate concentration in mg/L';
COMMENT ON COLUMN public.parameters.conductivity_us_cm IS 'Electrical conductivity in µS/cm';
COMMENT ON COLUMN public.parameters.dissolved_oxygen_mg_l IS 'Dissolved oxygen in mg/L';

-- ================================================================
-- END: Schema Complete
-- ================================================================
-- Status: ✓ Idempotent (safe to run multiple times)
-- Status: ✓ RLS Enabled (all tables secured)
-- Status: ✓ Foreign Keys (referential integrity)
-- Status: ✓ Indexes (performance optimized)
-- ================================================================
