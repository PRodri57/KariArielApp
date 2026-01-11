import { useEffect, useState } from "react";
import { format, parseISO } from "date-fns";
import { Link, useParams } from "react-router-dom";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Select } from "@/components/ui/Select";
import { Textarea } from "@/components/ui/Textarea";
import { StatusBadge } from "@/components/StatusBadge";
import { useOrden, useUpdateOrden } from "@/hooks/ordenes";
import type { OrdenEstado, OrdenUpdatePayload } from "@/lib/types";
import { ordenUpdateFormSchema, type OrdenUpdateFormValues } from "@/lib/validation";

export function OrdenDetalle() {
  const params = useParams();
  const numero = Number(params.numero);
  const { data: orden, isLoading } = useOrden(Number.isNaN(numero) ? undefined : numero);
  const updateOrden = useUpdateOrden();
  const [editando, setEditando] = useState(false);

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors }
  } = useForm<OrdenUpdateFormValues>({
    resolver: zodResolver(ordenUpdateFormSchema),
    defaultValues: {
      estado: "",
      fecha_retiro: "",
      problema: "",
      diagnostico: "",
      costo_estimado: "",
      costo_final: "",
      proveedor: "",
      sena: "",
      notas: ""
    }
  });

  useEffect(() => {
    if (!orden) return;
    reset({
      estado: orden.estado,
      fecha_retiro: orden.fecha_retiro ? orden.fecha_retiro.slice(0, 10) : "",
      problema: orden.problema ?? "",
      diagnostico: orden.diagnostico ?? "",
      costo_estimado:
        orden.costo_estimado !== null && orden.costo_estimado !== undefined
          ? String(orden.costo_estimado)
          : "",
      costo_final:
        orden.costo_final !== null && orden.costo_final !== undefined
          ? String(orden.costo_final)
          : "",
      proveedor: orden.proveedor ?? "",
      sena: orden.sena !== null && orden.sena !== undefined ? String(orden.sena) : "",
      notas: orden.notas ?? ""
    });
  }, [orden, reset]);

  const onSubmit = async (values: OrdenUpdateFormValues) => {
    if (!orden) return;
    const payload: OrdenUpdatePayload = {
      numero_orden: orden.numero_orden
    };

    if (values.estado) payload.estado = values.estado as OrdenEstado;
    if (values.fecha_retiro) payload.fecha_retiro = values.fecha_retiro;
    if (values.problema) payload.problema = values.problema;
    if (values.diagnostico) payload.diagnostico = values.diagnostico;
    if (values.costo_estimado) payload.costo_estimado = Number(values.costo_estimado);
    if (values.costo_final) payload.costo_final = Number(values.costo_final);
    if (values.proveedor) payload.proveedor = values.proveedor;
    if (values.sena) payload.sena = Number(values.sena);
    if (values.notas) payload.notas = values.notas;

    await updateOrden.mutateAsync(payload);
    setEditando(false);
  };

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
                <span className="font-semibold text-ink">
                  {orden.cliente_nombre ?? "Cliente sin datos"}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span>Equipo</span>
                <span className="font-semibold text-ink">
                  {orden.telefono_label ?? `Telefono #${orden.telefono_id}`}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span>Ingreso</span>
                <span className="font-semibold text-ink">
                  {format(parseISO(orden.fecha_ingreso), "dd MMM yyyy")}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span>Retiro</span>
                <span className="font-semibold text-ink">
                  {orden.fecha_retiro
                    ? format(parseISO(orden.fecha_retiro), "dd MMM yyyy")
                    : "-"}
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
              <div className="flex items-center justify-between">
                <span>Sena</span>
                <span className="font-semibold text-ink">
                  ${orden.sena ?? "-"}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span>Proveedor</span>
                <span className="font-semibold text-ink">
                  {orden.proveedor ?? "-"}
                </span>
              </div>
            </div>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Acciones</CardTitle>
            </CardHeader>
            <div className="flex flex-col gap-3">
              <Button variant="secondary" type="button">
                Marcar en proceso
              </Button>
              <Button variant="outline" type="button">
                Listo para retiro
              </Button>
              <Button variant="ghost" type="button">
                Cerrar orden
              </Button>
              <Button type="button" onClick={() => setEditando((prev) => !prev)}>
                {editando ? "Cancelar edicion" : "Editar orden"}
              </Button>
            </div>
          </Card>
        </div>
      ) : null}

      {orden && editando ? (
        <Card>
          <CardHeader>
            <CardTitle>Editar orden</CardTitle>
          </CardHeader>
          <form onSubmit={handleSubmit(onSubmit)} className="grid gap-4">
            <div className="grid gap-4 md:grid-cols-2">
              <div>
                <label className="text-sm font-semibold">Estado</label>
                <Select {...register("estado")}>
                  <option value="">Sin cambios</option>
                  <option value="ABIERTA">Abierta</option>
                  <option value="EN_PROCESO">En proceso</option>
                  <option value="ESPERANDO_REPUESTO">Esperando repuesto</option>
                  <option value="LISTA">Lista</option>
                  <option value="CERRADA">Cerrada</option>
                  <option value="CANCELADA">Cancelada</option>
                </Select>
              </div>
              <div>
                <label className="text-sm font-semibold">Fecha retiro</label>
                <Input type="date" {...register("fecha_retiro")} />
                {errors.fecha_retiro ? (
                  <p className="mt-1 text-xs text-ember">
                    {errors.fecha_retiro.message}
                  </p>
                ) : null}
              </div>
            </div>

            <div>
              <label className="text-sm font-semibold">Problema</label>
              <Textarea {...register("problema")} />
            </div>

            <div>
              <label className="text-sm font-semibold">Diagnostico</label>
              <Textarea {...register("diagnostico")} />
            </div>

            <div className="grid gap-4 md:grid-cols-2">
              <div>
                <label className="text-sm font-semibold">Costo estimado</label>
                <Input placeholder="15000" {...register("costo_estimado")} />
                {errors.costo_estimado ? (
                  <p className="mt-1 text-xs text-ember">
                    {errors.costo_estimado.message}
                  </p>
                ) : null}
              </div>
              <div>
                <label className="text-sm font-semibold">Costo final</label>
                <Input placeholder="20000" {...register("costo_final")} />
                {errors.costo_final ? (
                  <p className="mt-1 text-xs text-ember">
                    {errors.costo_final.message}
                  </p>
                ) : null}
              </div>
            </div>

            <div className="grid gap-4 md:grid-cols-2">
              <div>
                <label className="text-sm font-semibold">Proveedor</label>
                <Input placeholder="Proveedor" {...register("proveedor")} />
              </div>
              <div>
                <label className="text-sm font-semibold">Sena</label>
                <Input placeholder="5000" {...register("sena")} />
                {errors.sena ? (
                  <p className="mt-1 text-xs text-ember">{errors.sena.message}</p>
                ) : null}
              </div>
            </div>

            <div>
              <label className="text-sm font-semibold">Notas</label>
              <Textarea {...register("notas")} />
            </div>

            <div className="flex flex-wrap gap-2">
              <Button type="submit" disabled={updateOrden.isPending}>
                {updateOrden.isPending ? "Guardando..." : "Guardar cambios"}
              </Button>
              <Button
                type="button"
                variant="ghost"
                onClick={() => setEditando(false)}
              >
                Cancelar
              </Button>
            </div>
          </form>
        </Card>
      ) : null}
    </div>
  );
}
