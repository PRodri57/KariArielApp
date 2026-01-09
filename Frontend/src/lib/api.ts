import type { Orden, OrdenCreatePayload, OrdenCreateResponse } from "@/lib/types";

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? "";
const USE_MOCKS = import.meta.env.VITE_USE_MOCKS === "true" || !API_BASE;

const wait = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

let mockSequence = 18023;
const mockOrders: Orden[] = [
  {
    id: 1,
    numero_orden: 18021,
    cliente: "Marta R.",
    telefono: "iPhone 12",
    estado: "EN_PROCESO",
    fecha_ingreso: "2024-12-28",
    problema: "Pantalla rota",
    costo_estimado: 32000
  },
  {
    id: 2,
    numero_orden: 18022,
    cliente: "Luis G.",
    telefono: "Samsung A52",
    estado: "ABIERTA",
    fecha_ingreso: "2024-12-30",
    problema: "No enciende",
    costo_estimado: 18500
  }
];

async function fetchJson<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...init
  });

  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || "API error");
  }

  return response.json() as Promise<T>;
}

export async function listOrdenes(): Promise<Orden[]> {
  if (USE_MOCKS) {
    await wait(400);
    return [...mockOrders];
  }

  return fetchJson<Orden[]>("/ordenes_trabajo");
}

export async function getOrden(numero: number): Promise<Orden | null> {
  if (USE_MOCKS) {
    await wait(300);
    return mockOrders.find((orden) => orden.numero_orden === numero) ?? null;
  }

  return fetchJson<Orden>(`/ordenes_trabajo/${numero}`);
}

export async function createOrden(
  payload: OrdenCreatePayload
): Promise<OrdenCreateResponse> {
  if (USE_MOCKS) {
    await wait(500);
    const numero_orden = mockSequence++;
    mockOrders.unshift({
      id: mockOrders.length + 1,
      numero_orden,
      cliente: payload.cliente,
      telefono: `${payload.telefono_marca} ${payload.telefono_modelo}`,
      estado: "ABIERTA",
      fecha_ingreso: new Date().toISOString().slice(0, 10),
      problema: payload.problema,
      costo_estimado: payload.costo_estimado ?? null
    });
    return { numero_orden };
  }

  return fetchJson<OrdenCreateResponse>("/ordenes_trabajo", {
    method: "POST",
    body: JSON.stringify(payload)
  });
}
