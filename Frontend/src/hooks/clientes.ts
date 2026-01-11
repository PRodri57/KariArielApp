import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { createCliente, getCliente, listClientes } from "@/lib/api";
import type { ClienteCreatePayload } from "@/lib/types";

export function useClientes() {
  return useQuery({
    queryKey: ["clientes"],
    queryFn: listClientes
  });
}

export function useCliente(id?: number) {
  return useQuery({
    queryKey: ["clientes", id],
    queryFn: () => (id ? getCliente(id) : Promise.resolve(null)),
    enabled: Boolean(id)
  });
}

export function useCreateCliente() {
  const client = useQueryClient();

  return useMutation({
    mutationFn: (payload: ClienteCreatePayload) => createCliente(payload),
    onSuccess: () => {
      client.invalidateQueries({ queryKey: ["clientes"] });
    }
  });
}
