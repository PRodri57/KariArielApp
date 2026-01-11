import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { createOrden, getOrden, listOrdenes, updateOrden } from "@/lib/api";
import type { OrdenCreatePayload, OrdenUpdatePayload } from "@/lib/types";

export function useOrdenes() {
  return useQuery({
    queryKey: ["ordenes"],
    queryFn: listOrdenes
  });
}

export function useOrden(numero?: number) {
  return useQuery({
    queryKey: ["orden", numero],
    queryFn: () => (numero ? getOrden(numero) : Promise.resolve(null)),
    enabled: Boolean(numero)
  });
}

export function useCreateOrden() {
  const client = useQueryClient();

  return useMutation({
    mutationFn: (payload: OrdenCreatePayload) => createOrden(payload),
    onSuccess: () => {
      client.invalidateQueries({ queryKey: ["ordenes"] });
    }
  });
}

export function useUpdateOrden() {
  const client = useQueryClient();

  return useMutation({
    mutationFn: (payload: OrdenUpdatePayload) => updateOrden(payload),
    onSuccess: (data) => {
      client.invalidateQueries({ queryKey: ["ordenes"] });
      client.invalidateQueries({ queryKey: ["orden", data.numero_orden] });
    }
  });
}
