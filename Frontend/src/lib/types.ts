export type OrdenEstado =
  | "ABIERTA"
  | "EN_PROCESO"
  | "ESPERANDO_REPUESTO"
  | "LISTA"
  | "CERRADA"
  | "CANCELADA";

export type Orden = {
  id: number;
  numero_orden: number;
  cliente: string;
  telefono: string;
  estado: OrdenEstado;
  fecha_ingreso: string;
  problema: string;
  costo_estimado?: number | null;
};

export type OrdenCreatePayload = {
  cliente: string;
  telefono_marca: string;
  telefono_modelo: string;
  telefono_imei?: string;
  problema: string;
  diagnostico?: string;
  costo_estimado?: number;
  notas?: string;
};

export type OrdenCreateResponse = {
  numero_orden: number;
};
