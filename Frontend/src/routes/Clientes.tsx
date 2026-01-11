import { useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { Input } from "@/components/ui/Input";
import { useClientes } from "@/hooks/clientes";
import { useTelefonos } from "@/hooks/telefonos";

export function Clientes() {
  const { data: clientes = [], isLoading } = useClientes();
  const { data: telefonos = [] } = useTelefonos();
  const [query, setQuery] = useState("");

  const telefonosPorCliente = useMemo(() => {
    const map = new Map<number, number>();
    telefonos.forEach((telefono) => {
      map.set(telefono.cliente_id, (map.get(telefono.cliente_id) ?? 0) + 1);
    });
    return map;
  }, [telefonos]);

  const filtrados = useMemo(() => {
    const term = query.trim().toLowerCase();
    if (!term) return clientes;
    return clientes.filter((cliente) => {
      const nombre = cliente.nombre.toLowerCase();
      const dni = cliente.dni ?? "";
      const telefono = cliente.telefono_contacto ?? "";
      const email = cliente.email ?? "";
      return (
        nombre.includes(term) ||
        dni.toLowerCase().includes(term) ||
        telefono.toLowerCase().includes(term) ||
        email.toLowerCase().includes(term)
      );
    });
  }, [clientes, query]);

  return (
    <div className="flex flex-col gap-6">
      <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div>
          <h2 className="text-3xl">Clientes</h2>
          <p className="text-sm text-ink/60">
            Administra clientes y accede a sus equipos.
          </p>
        </div>
        <div className="flex flex-col gap-3 md:flex-row md:items-center">
          <Input
            placeholder="Buscar por nombre, DNI, telefono o email"
            value={query}
            onChange={(event) => setQuery(event.target.value)}
          />
          <Link to="/clientes/nuevo">
            <Button size="md">Nuevo cliente</Button>
          </Link>
        </div>
      </div>

      <Card className="overflow-hidden p-0">
        <div className="grid grid-cols-4 gap-2 border-b border-ink/10 bg-haze/70 px-6 py-4 text-xs uppercase tracking-[0.3em] text-ink/40">
          <span>Cliente</span>
          <span>DNI</span>
          <span>Contacto</span>
          <span>Telefonos</span>
        </div>
        <div className="divide-y divide-ink/10">
          {isLoading ? (
            <div className="px-6 py-8 text-sm text-ink/60">Cargando...</div>
          ) : null}
          {!isLoading && filtrados.length === 0 ? (
            <div className="px-6 py-8 text-sm text-ink/60">
              No hay clientes para mostrar.
            </div>
          ) : null}
          {filtrados.map((cliente) => (
            <Link
              key={cliente.id}
              to={`/clientes/${cliente.id}`}
              className="grid grid-cols-1 gap-2 px-6 py-4 text-sm transition hover:bg-ink/5 md:grid-cols-4"
            >
              <span className="font-semibold text-ink">{cliente.nombre}</span>
              <span className="text-ink/70">{cliente.dni ?? "-"}</span>
              <span className="text-ink/70">{cliente.telefono_contacto ?? "-"}</span>
              <span className="text-ink/70">
                {telefonosPorCliente.get(cliente.id) ?? 0}
              </span>
            </Link>
          ))}
        </div>
      </Card>
    </div>
  );
}
