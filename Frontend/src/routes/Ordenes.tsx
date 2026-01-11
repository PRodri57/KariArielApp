import { useMemo, useState } from "react";
import { format, parseISO } from "date-fns";
import { Link } from "react-router-dom";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { StatusBadge } from "@/components/StatusBadge";
import { useOrdenes } from "@/hooks/ordenes";
import type { OrdenEstado } from "@/lib/types";

const filtros: Array<{ label: string; value: OrdenEstado | "TODAS" }> = [
  { label: "Todas", value: "TODAS" },
  { label: "Abiertas", value: "ABIERTA" },
  { label: "En proceso", value: "EN_PROCESO" },
  { label: "Listas", value: "LISTA" }
];

export function Ordenes() {
  const { data: ordenes = [], isLoading } = useOrdenes();
  const [filtro, setFiltro] = useState<OrdenEstado | "TODAS">("TODAS");

  const lista = useMemo(() => {
    if (filtro === "TODAS") return ordenes;
    return ordenes.filter((orden) => orden.estado === filtro);
  }, [ordenes, filtro]);

  return (
    <div className="flex flex-col gap-6">
      <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div>
          <h2 className="text-3xl">Ordenes</h2>
        </div>
        <div className="flex flex-wrap gap-2">
          {filtros.map((item) => (
            <Button
              key={item.value}
              size="sm"
              variant={filtro === item.value ? "secondary" : "outline"}
              onClick={() => setFiltro(item.value)}
            >
              {item.label}
            </Button>
          ))}
        </div>
      </div>

      <Card className="overflow-hidden p-0">
        <div className="grid grid-cols-7 gap-2 border-b border-ink/10 bg-haze/70 px-6 py-4 text-xs uppercase tracking-[0.3em] text-ink/40">
          <span>Orden</span>
          <span>Cliente</span>
          <span>Equipo</span>
          <span>Estado</span>
          <span>Ingreso</span>
          <span>Retiro</span>
          <span>Proveedor</span>
        </div>
        <div className="divide-y divide-ink/10">
          {isLoading ? (
            <div className="px-6 py-8 text-sm text-ink/60">Cargando...</div>
          ) : null}
          {!isLoading && lista.length === 0 ? (
            <div className="px-6 py-8 text-sm text-ink/60">
              No hay ordenes para este filtro.
            </div>
          ) : null}
          {lista.map((orden) => (
            <Link
              key={orden.numero_orden}
              to={`/ordenes/${orden.numero_orden}`}
              className="grid grid-cols-1 gap-2 px-6 py-4 text-sm transition hover:bg-ink/5 md:grid-cols-7"
            >
              <span className="font-semibold text-ink">
                #{orden.numero_orden}
              </span>
              <span className="text-ink/70">
                {orden.cliente_nombre ?? "Cliente sin datos"}
              </span>
              <span className="text-ink/70">
                {orden.telefono_label ?? `Telefono #${orden.telefono_id}`}
              </span>
              <StatusBadge estado={orden.estado} />
              <span className="text-ink/60">
                {format(parseISO(orden.fecha_ingreso), "dd/MM/yyyy")}
              </span>
              <span className="text-ink/60">
                {orden.fecha_retiro
                  ? format(parseISO(orden.fecha_retiro), "dd/MM/yyyy")
                  : "-"}
              </span>
              <span className="text-ink/60">{orden.proveedor ?? "-"}</span>
            </Link>
          ))}
        </div>
      </Card>
    </div>
  );
}
