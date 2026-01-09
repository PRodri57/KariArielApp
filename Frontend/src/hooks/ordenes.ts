import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { createOrden, getOrden, listOrdenes } from "@/lib/api";
import type { OrdenCreatePayload } from "@/lib/types";

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
