import type {
  Cliente,
  ClienteCreatePayload,
  ClienteCreateResponse,
  Orden,
  OrdenCreatePayload,
  OrdenCreateResponse,
  OrdenEstado,
  OrdenUpdatePayload,
  Telefono,
  TelefonoCreatePayload,
  TelefonoCreateResponse,
  TelefonoUpdatePayload
} from "@/lib/types";

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? "";
const USE_MOCKS = import.meta.env.VITE_USE_MOCKS === "true" || !API_BASE;

const wait = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

let mockClienteId = 4;
let mockTelefonoId = 5;
let mockOrdenId = 3;
let mockSequence = 18023;

const mockClientes: Cliente[] = [
  {
    id: 1,
    dni: "23456789",
    nombre: "Marta R.",
    telefono_contacto: "11 5555-1234",
    notas: "Prefiere WhatsApp.",
    creado_en: "2024-12-10"
  },
  {
    id: 2,
    dni: "29123456",
    nombre: "Luis G.",
    telefono_contacto: "11 4222-9012",
    notas: null,
    creado_en: "2024-12-15"
  },
  {
    id: 3,
    dni: null,
    nombre: "Sofia L.",
    telefono_contacto: "11 6000-7788",
    notas: "Trabaja cerca del local.",
    creado_en: "2024-12-18"
  }
];

const mockTelefonos: Telefono[] = [
  {
    id: 1,
    cliente_id: 1,
    marca: "Apple",
    modelo: "iPhone 12",
    notas: "Pantalla quebrada.",
    creado_en: "2024-12-10"
  },
  {
    id: 2,
    cliente_id: 2,
    marca: "Samsung",
    modelo: "A52",
    notas: null,
    creado_en: "2024-12-15"
  },
  {
    id: 3,
    cliente_id: 2,
    marca: "Motorola",
    modelo: "G62",
    notas: "Equipo de respaldo.",
    creado_en: "2024-12-20"
  },
  {
    id: 4,
    cliente_id: 3,
    marca: "Xiaomi",
    modelo: "Note 12",
    notas: null,
    creado_en: "2024-12-21"
  }
];

const mockOrdenes: Orden[] = [
  {
    id: 1,
    numero_orden: 18021,
    telefono_id: 1,
    cliente_id: 1,
    estado: "EN_PROCESO",
    fecha_ingreso: "2024-12-28",
    fecha_retiro: null,
    problema: "Pantalla rota",
    diagnostico: "Flex dañado",
    costo_estimado: 32000,
    proveedor: "Proveedor Central",
    sena: 5000
  },
  {
    id: 2,
    numero_orden: 18022,
    telefono_id: 2,
    cliente_id: 2,
    estado: "ABIERTA",
    fecha_ingreso: "2024-12-30",
    fecha_retiro: null,
    problema: "No enciende",
    diagnostico: null,
    costo_estimado: 18500,
    proveedor: null,
    sena: null
  }
];

const telefonoLabel = (telefono: Telefono) => `${telefono.marca} ${telefono.modelo}`;

const withOrdenLabels = (orden: Orden): Orden => {
  const telefono = mockTelefonos.find((item) => item.id === orden.telefono_id);
  const cliente = telefono
    ? mockClientes.find((item) => item.id === telefono.cliente_id)
    : null;
  return {
    ...orden,
    cliente_id: cliente?.id ?? orden.cliente_id ?? null,
    cliente_nombre: cliente?.nombre ?? null,
    telefono_label: telefono ? telefonoLabel(telefono) : null
  };
};

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

export async function listClientes(): Promise<Cliente[]> {
  if (USE_MOCKS) {
    await wait(300);
    return [...mockClientes];
  }

  return fetchJson<Cliente[]>("/clientes");
}

export async function getCliente(id: number): Promise<Cliente | null> {
  if (USE_MOCKS) {
    await wait(200);
    return mockClientes.find((cliente) => cliente.id === id) ?? null;
  }

  return fetchJson<Cliente>(`/clientes/${id}`);
}

export async function createCliente(
  payload: ClienteCreatePayload
): Promise<ClienteCreateResponse> {
  if (USE_MOCKS) {
    await wait(400);
    const nuevo: Cliente = {
      id: mockClienteId++,
      nombre: payload.nombre,
      dni: payload.dni ?? null,
      telefono_contacto: payload.telefono_contacto ?? null,
      notas: payload.notas ?? null,
      creado_en: new Date().toISOString().slice(0, 10)
    };
    mockClientes.unshift(nuevo);
    return { id: nuevo.id };
  }

  return fetchJson<ClienteCreateResponse>("/clientes", {
    method: "POST",
    body: JSON.stringify(payload)
  });
}

export async function listTelefonos(clienteId?: number): Promise<Telefono[]> {
  if (USE_MOCKS) {
    await wait(250);
    const lista = clienteId
      ? mockTelefonos.filter((telefono) => telefono.cliente_id === clienteId)
      : mockTelefonos;
    return [...lista];
  }

  const query = clienteId ? `?cliente_id=${clienteId}` : "";
  return fetchJson<Telefono[]>(`/telefonos${query}`);
}

export async function createTelefono(
  payload: TelefonoCreatePayload
): Promise<TelefonoCreateResponse> {
  if (USE_MOCKS) {
    await wait(350);
    const nuevo: Telefono = {
      id: mockTelefonoId++,
      cliente_id: payload.cliente_id,
      marca: payload.marca,
      modelo: payload.modelo,
      notas: payload.notas ?? null,
      creado_en: new Date().toISOString().slice(0, 10)
    };
    mockTelefonos.unshift(nuevo);
    return { id: nuevo.id };
  }

  return fetchJson<TelefonoCreateResponse>("/telefonos", {
    method: "POST",
    body: JSON.stringify(payload)
  });
}

export async function updateTelefono(
  payload: TelefonoUpdatePayload
): Promise<Telefono> {
  if (USE_MOCKS) {
    await wait(300);
    const index = mockTelefonos.findIndex((item) => item.id === payload.id);
    if (index === -1) {
      throw new Error("Telefono no encontrado");
    }
    const actualizado: Telefono = {
      ...mockTelefonos[index],
      marca: payload.marca,
      modelo: payload.modelo,
      notas: payload.notas ?? null
    };
    mockTelefonos[index] = actualizado;
    return actualizado;
  }

  return fetchJson<Telefono>(`/telefonos/${payload.id}`, {
    method: "PUT",
    body: JSON.stringify(payload)
  });
}

export async function listOrdenes(): Promise<Orden[]> {
  if (USE_MOCKS) {
    await wait(400);
    return mockOrdenes.map(withOrdenLabels);
  }

  return fetchJson<Orden[]>("/ordenes_trabajo");
}

export async function getOrden(numero: number): Promise<Orden | null> {
  if (USE_MOCKS) {
    await wait(300);
    const orden = mockOrdenes.find((item) => item.numero_orden === numero);
    return orden ? withOrdenLabels(orden) : null;
  }

  return fetchJson<Orden>(`/ordenes_trabajo/${numero}`);
}

export async function createOrden(
  payload: OrdenCreatePayload
): Promise<OrdenCreateResponse> {
  if (USE_MOCKS) {
    await wait(500);
    const telefono = mockTelefonos.find(
      (item) => item.id === payload.telefono_id
    );
    if (!telefono) {
      throw new Error("Telefono no existe");
    }
    const numero_orden = mockSequence++;
    const estado: OrdenEstado = "ABIERTA";
    mockOrdenes.unshift({
      id: mockOrdenId++,
      numero_orden,
      telefono_id: payload.telefono_id,
      cliente_id: telefono.cliente_id,
      estado,
      fecha_ingreso: new Date().toISOString().slice(0, 10),
      fecha_retiro: null,
      problema: payload.problema,
      diagnostico: payload.diagnostico ?? null,
      costo_estimado: payload.costo_estimado ?? null,
      proveedor: payload.proveedor ?? null,
      sena: payload.sena ?? null,
      notas: payload.notas ?? null
    });
    return { numero_orden };
  }

  return fetchJson<OrdenCreateResponse>("/ordenes_trabajo", {
    method: "POST",
    body: JSON.stringify(payload)
  });
}

export async function updateOrden(payload: OrdenUpdatePayload): Promise<Orden> {
  if (USE_MOCKS) {
    await wait(350);
    const index = mockOrdenes.findIndex(
      (item) => item.numero_orden === payload.numero_orden
    );
    if (index === -1) {
      throw new Error("Orden no encontrada");
    }
    const current = mockOrdenes[index];
    const actualizado: Orden = {
      ...current,
      estado: payload.estado ?? current.estado,
      fecha_retiro:
        payload.fecha_retiro !== undefined
          ? payload.fecha_retiro
          : current.fecha_retiro ?? null,
      problema: payload.problema ?? current.problema,
      diagnostico:
        payload.diagnostico !== undefined
          ? payload.diagnostico
          : current.diagnostico ?? null,
      costo_estimado:
        payload.costo_estimado !== undefined
          ? payload.costo_estimado
          : current.costo_estimado ?? null,
      costo_final:
        payload.costo_final !== undefined
          ? payload.costo_final
          : current.costo_final ?? null,
      proveedor:
        payload.proveedor !== undefined
          ? payload.proveedor
          : current.proveedor ?? null,
      sena:
        payload.sena !== undefined ? payload.sena : current.sena ?? null,
      notas:
        payload.notas !== undefined ? payload.notas : current.notas ?? null
    };
    mockOrdenes[index] = actualizado;
    return withOrdenLabels(actualizado);
  }

  return fetchJson<Orden>(`/ordenes_trabajo/${payload.numero_orden}`, {
    method: "PUT",
    body: JSON.stringify(payload)
  });
}
