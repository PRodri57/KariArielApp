import { format, parseISO } from "date-fns";
import { Link } from "react-router-dom";
import { Card, CardDescription, CardHeader, CardTitle } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { StatusBadge } from "@/components/StatusBadge";
import { useClientes } from "@/hooks/clientes";
import { useOrdenes } from "@/hooks/ordenes";
import { useTelefonos } from "@/hooks/telefonos";

export function Dashboard() {
  const { data: ordenes = [], isLoading } = useOrdenes();
  const { data: clientes = [], isLoading: clientesLoading } = useClientes();
  const { data: telefonos = [], isLoading: telefonosLoading } = useTelefonos();

  const abiertas = ordenes.filter((orden) => orden.estado === "ABIERTA").length;
  const enProceso = ordenes.filter((orden) => orden.estado === "EN_PROCESO").length;
  const listas = ordenes.filter((orden) => orden.estado === "LISTA").length;

  return (
    <div className="flex flex-col gap-6">
      <div className="grid gap-4 md:grid-cols-5">
        <Card>
          <CardHeader>
            <CardDescription>Abiertas</CardDescription>
            <CardTitle>{isLoading ? "..." : abiertas}</CardTitle>
          </CardHeader>
        </Card>
        <Card>
          <CardHeader>
            <CardDescription>En proceso</CardDescription>
            <CardTitle>{isLoading ? "..." : enProceso}</CardTitle>
          </CardHeader>
        </Card>
        <Card>
          <CardHeader>
            <CardDescription>Listas</CardDescription>
            <CardTitle>{isLoading ? "..." : listas}</CardTitle>
          </CardHeader>
        </Card>
        <Card>
          <CardHeader>
            <CardDescription>Clientes</CardDescription>
            <CardTitle>{clientesLoading ? "..." : clientes.length}</CardTitle>
          </CardHeader>
        </Card>
        <Card>
          <CardHeader>
            <CardDescription>Telefonos</CardDescription>
            <CardTitle>{telefonosLoading ? "..." : telefonos.length}</CardTitle>
          </CardHeader>
        </Card>
      </div>

      <Card className="overflow-hidden">
        <CardHeader className="flex flex-row items-center justify-between">
          <CardTitle>Ordenes recientes</CardTitle>
          <Link to="/ordenes">
            <Button size="sm" variant="outline">
              Ver todas
            </Button>
          </Link>
        </CardHeader>

          <div className="divide-y divide-ink/10">
            {ordenes.slice(0, 4).map((orden) => (
              <div
                key={orden.numero_orden}
                className="flex flex-col gap-3 px-2 py-4 md:flex-row md:items-center md:justify-between"
              >
                <div>
                  <p className="text-sm text-ink/60">Orden #{orden.numero_orden}</p>
                  <p className="text-base font-semibold text-ink">
                    {orden.cliente_nombre ?? "Cliente sin datos"} -{" "}
                    {orden.telefono_label ?? `Telefono #${orden.telefono_id}`}
                  </p>
                  <p className="text-xs text-ink/50">
                    {format(parseISO(orden.fecha_ingreso), "dd MMM yyyy")}
                  </p>
                </div>
                <div className="flex items-center gap-3">
                  <StatusBadge estado={orden.estado} />
                  <span className="text-sm font-semibold text-ink">
                    ${orden.costo_estimado ?? "-"}
                  </span>
                </div>
              </div>
            ))}

            {!ordenes.length && !isLoading ? (
              <div className="px-4 py-8 text-center text-sm text-ink/50">
                Aun no hay ordenes cargadas.
              </div>
            ) : null}
          </div>
      </Card>
    </div>
  );
}
