import { format, parseISO } from "date-fns";
import { Link, useParams } from "react-router-dom";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { StatusBadge } from "@/components/StatusBadge";
import { useOrden } from "@/hooks/ordenes";

export function OrdenDetalle() {
  const params = useParams();
  const numero = Number(params.numero);
  const { data: orden, isLoading } = useOrden(Number.isNaN(numero) ? undefined : numero);

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div>
          <p className="text-xs uppercase tracking-[0.3em] text-ink/50">
            Orden de trabajo
          </p>
          <h2 className="text-3xl">#{params.numero}</h2>
        </div>
        <Link to="/ordenes">
          <Button variant="outline">Volver a ordenes</Button>
        </Link>
      </div>

      {isLoading ? (
        <Card>
          <p className="text-sm text-ink/60">Cargando...</p>
        </Card>
      ) : null}

      {!isLoading && !orden ? (
        <Card>
          <p className="text-sm text-ink/60">No se encontro la orden.</p>
        </Card>
      ) : null}

      {orden ? (
        <div className="grid gap-6 lg:grid-cols-[2fr_1fr]">
          <Card>
            <CardHeader>
              <CardTitle>Resumen</CardTitle>
            </CardHeader>
            <div className="grid gap-4 text-sm text-ink/70">
              <div className="flex items-center justify-between">
                <span>Cliente</span>
                <span className="font-semibold text-ink">{orden.cliente}</span>
              </div>
              <div className="flex items-center justify-between">
                <span>Equipo</span>
                <span className="font-semibold text-ink">{orden.telefono}</span>
              </div>
              <div className="flex items-center justify-between">
                <span>Ingreso</span>
                <span className="font-semibold text-ink">
                  {format(parseISO(orden.fecha_ingreso), "dd MMM yyyy")}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span>Estado</span>
                <StatusBadge estado={orden.estado} />
              </div>
              <div className="flex items-center justify-between">
                <span>Costo estimado</span>
                <span className="font-semibold text-ink">
                  ${orden.costo_estimado ?? "-"}
                </span>
              </div>
            </div>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Acciones</CardTitle>
            </CardHeader>
            <div className="flex flex-col gap-3">
              <Button variant="secondary">Marcar en proceso</Button>
              <Button variant="outline">Listo para retiro</Button>
              <Button variant="ghost">Cerrar orden</Button>
            </div>
          </Card>
        </div>
      ) : null}
    </div>
  );
}
