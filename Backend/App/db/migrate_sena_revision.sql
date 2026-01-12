-- Migrate sena_revision into sena + ordenes_senas history.
-- Run this in Supabase SQL editor (or psql) once.

-- 1) Insert sena_revision into history (use order created_at as timestamp).
INSERT INTO public.ordenes_senas (orden_id, monto, created_at)
SELECT id, sena_revision, created_at
FROM public.ordenes_de_trabajo
WHERE sena_revision IS NOT NULL AND sena_revision > 0;

-- 2) Add sena_revision to the total sena value.
UPDATE public.ordenes_de_trabajo
SET sena = COALESCE(sena, 0) + COALESCE(sena_revision, 0)
WHERE sena_revision IS NOT NULL AND sena_revision > 0;

-- 3) Clear sena_revision to avoid double counting.
UPDATE public.ordenes_de_trabajo
SET sena_revision = NULL
WHERE sena_revision IS NOT NULL AND sena_revision > 0;
