-- WARNING: This schema is for context only and is not meant to be run.
-- Table order and constraints may not be valid for execution.

CREATE TABLE public.clientes (
  id bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  dni bigint NOT NULL UNIQUE,
  nyape text,
  tel_contacto text,
  email text,
  notas text,
  created_at timestamp with time zone DEFAULT now(),
  CONSTRAINT clientes_pkey PRIMARY KEY (id)
);
CREATE TABLE public.ordenes_de_trabajo (
  id bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  num_orden bigint GENERATED ALWAYS AS IDENTITY NOT NULL UNIQUE,
  tel_id bigint,
  estado smallint,
  ingreso date DEFAULT now(),
  retiro date,
  problema text,
  diagnostico text,
  presupuesto bigint,
  costo_bruto numeric,
  garantia integer DEFAULT 30,
  senia bigint,
  notas text,
  proveedor text,
  sena numeric,
  costo_revision numeric,
  sena_revision numeric,
  CONSTRAINT ordenes_de_trabajo_pkey PRIMARY KEY (id),
  CONSTRAINT ordenes_de_trabajo_tel_id_fkey FOREIGN KEY (tel_id) REFERENCES public.telefonos(id)
);
CREATE TABLE public.ordenes_senas (
  id bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  orden_id bigint NOT NULL,
  monto numeric NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT ordenes_senas_pkey PRIMARY KEY (id),
  CONSTRAINT ordenes_senas_orden_id_fkey FOREIGN KEY (orden_id) REFERENCES public.ordenes_de_trabajo(id)
);
CREATE TABLE public.telefonos (
  id bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  cliente_id bigint,
  marca text,
  modelo text,
  color text,
  notas text,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  updated_at timestamp with time zone DEFAULT now(),
  CONSTRAINT telefonos_pkey PRIMARY KEY (id),
  CONSTRAINT telefonos_cliente_id_fkey FOREIGN KEY (cliente_id) REFERENCES public.clientes(id)
);
