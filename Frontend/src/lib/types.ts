export type OrdenEstado =
  | "ABIERTA"
  | "EN_PROCESO"
  | "ESPERANDO_REPUESTO"
  | "LISTA"
  | "CERRADA"
  | "CANCELADA";

export type Cliente = {
  id: number;
  dni?: string | null;
  nombre: string;
  telefono_contacto?: string | null;
  notas?: string | null;
  creado_en: string;
};

export type Telefono = {
  id: number;
  cliente_id: number;
  marca: string;
  modelo: string;
  notas?: string | null;
  creado_en: string;
};

export type Orden = {
  id: number;
  numero_orden: number;
  telefono_id: number;
  cliente_id?: number | null;
  estado: OrdenEstado;
  fecha_ingreso: string;
  fecha_retiro?: string | null;
  problema: string;
  diagnostico?: string | null;
  costo_estimado?: number | null;
  costo_final?: number | null;
  proveedor?: string | null;
  sena?: number | null;
  notas?: string | null;
  cliente_nombre?: string | null;
  telefono_label?: string | null;
};

export type OrdenCreatePayload = {
  telefono_id: number;
  problema: string;
  diagnostico?: string;
  costo_estimado?: number;
  proveedor?: string;
  sena?: number;
  notas?: string;
};

export type OrdenCreateResponse = {
  numero_orden: number;
};

export type OrdenUpdatePayload = {
  numero_orden: number;
  estado?: OrdenEstado;
  fecha_retiro?: string;
  problema?: string;
  diagnostico?: string;
  costo_estimado?: number;
  costo_final?: number;
  proveedor?: string;
  sena?: number;
  notas?: string;
};

export type ClienteCreatePayload = {
  nombre: string;
  dni?: string;
  telefono_contacto?: string;
  notas?: string;
};

export type ClienteCreateResponse = {
  id: number;
};

export type TelefonoCreatePayload = {
  cliente_id: number;
  marca: string;
  modelo: string;
  notas?: string;
};

export type TelefonoCreateResponse = {
  id: number;
};

export type TelefonoUpdatePayload = {
  id: number;
  marca: string;
  modelo: string;
  notas?: string;
};
