import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { createTelefono, listTelefonos, updateTelefono } from "@/lib/api";
import type { TelefonoCreatePayload, TelefonoUpdatePayload } from "@/lib/types";

export function useTelefonos(clienteId?: number) {
  return useQuery({
    queryKey: ["telefonos", clienteId ?? "all"],
    queryFn: () => listTelefonos(clienteId)
  });
}

export function useCreateTelefono() {
  const client = useQueryClient();

  return useMutation({
    mutationFn: (payload: TelefonoCreatePayload) => createTelefono(payload),
    onSuccess: (_data, variables) => {
      client.invalidateQueries({ queryKey: ["telefonos"] });
      client.invalidateQueries({ queryKey: ["telefonos", variables.cliente_id] });
    }
  });
}

export function useUpdateTelefono() {
  const client = useQueryClient();

  return useMutation({
    mutationFn: (payload: TelefonoUpdatePayload) => updateTelefono(payload),
    onSuccess: (data) => {
      client.invalidateQueries({ queryKey: ["telefonos"] });
      client.invalidateQueries({ queryKey: ["telefonos", data.cliente_id] });
    }
  });
}
