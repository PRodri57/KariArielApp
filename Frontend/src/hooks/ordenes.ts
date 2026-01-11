import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  createOrden,
  createOrdenSena,
  deleteOrden,
  getOrden,
  listOrdenes,
  listOrdenSenas,
  updateOrden
} from "@/lib/api";
import type {
  OrdenCreatePayload,
  OrdenSenaCreatePayload,
  OrdenUpdatePayload
} from "@/lib/types";

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
      client.setQueryData(["orden", data.numero_orden], data);
      client.setQueryData(["ordenes"], (current) => {
        if (!Array.isArray(current)) return current;
        return current.map((orden) =>
          orden.numero_orden === data.numero_orden ? data : orden
        );
      });
      client.invalidateQueries({ queryKey: ["ordenes"] });
      client.invalidateQueries({ queryKey: ["orden", data.numero_orden] });
    }
  });
}

export function useOrdenSenas(numero?: number) {
  return useQuery({
    queryKey: ["orden", numero, "senas"],
    queryFn: () => (numero ? listOrdenSenas(numero) : Promise.resolve([])),
    enabled: Boolean(numero)
  });
}

export function useCreateOrdenSena() {
  const client = useQueryClient();

  return useMutation({
    mutationFn: ({
      numero,
      payload
    }: {
      numero: number;
      payload: OrdenSenaCreatePayload;
    }) => createOrdenSena(numero, payload),
    onSuccess: (_data, variables) => {
      client.invalidateQueries({ queryKey: ["orden", variables.numero, "senas"] });
      client.invalidateQueries({ queryKey: ["orden", variables.numero] });
      client.invalidateQueries({ queryKey: ["ordenes"] });
    }
  });
}

export function useDeleteOrden() {
  const client = useQueryClient();

  return useMutation({
    mutationFn: (numero: number) => deleteOrden(numero),
    onSuccess: (_data, numero) => {
      client.invalidateQueries({ queryKey: ["ordenes"] });
      client.removeQueries({ queryKey: ["orden", numero] });
      client.removeQueries({ queryKey: ["orden", numero, "senas"] });
    }
  });
}
