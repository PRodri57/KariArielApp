import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { createCliente, deleteCliente, getCliente, listClientes } from "@/lib/api";
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

export function useDeleteCliente() {
  const client = useQueryClient();

  return useMutation({
    mutationFn: (id: number) => deleteCliente(id),
    onSuccess: (_data, id) => {
      client.invalidateQueries({ queryKey: ["clientes"] });
      client.removeQueries({ queryKey: ["clientes", id] });
      client.invalidateQueries({ queryKey: ["telefonos"] });
    }
  });
}
