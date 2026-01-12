-- Add garantia to ordenes_de_trabajo with default 30.
-- Run this in Supabase SQL editor (or psql) once.

ALTER TABLE public.ordenes_de_trabajo
ADD COLUMN IF NOT EXISTS garantia integer NOT NULL DEFAULT 30;
