import { useEffect, useState } from "react";
import { format, parseISO } from "date-fns";
import { Link, useNavigate, useParams } from "react-router-dom";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Select } from "@/components/ui/Select";
import { Textarea } from "@/components/ui/Textarea";
import { StatusBadge } from "@/components/StatusBadge";
import { useCreateOrdenSena, useDeleteOrden, useOrden, useOrdenSenas, useUpdateOrden } from "@/hooks/ordenes";
import { useCliente } from "@/hooks/clientes";
import type { OrdenEstado, OrdenSenaCreatePayload, OrdenUpdatePayload } from "@/lib/types";
import { ordenUpdateFormSchema, type OrdenUpdateFormValues } from "@/lib/validation";

const proveedores = [
  "JV",
  "WorldCell",
  "Suma",
  "Jony",
  "SP",
  "CyA",
  "JK",
  "Sunlong",
  "Mercadolibre",
  "Premiumcell",
  "Saracell",
  "RV",
  "Electronica Martinez",
  "Otros..."
];

const API_BASE = (import.meta.env.VITE_API_BASE_URL ?? "").replace(/\/$/, "");
const USE_MOCKS =
  import.meta.env.VITE_USE_MOCKS === "true" || API_BASE.length === 0;

export function OrdenDetalle() {
  const params = useParams();
  const numero = Number(params.numero);
  const { data: orden, isLoading } = useOrden(Number.isNaN(numero) ? undefined : numero);
  const { data: cliente } = useCliente(orden?.cliente_id ?? undefined);
  const { data: senas = [] } = useOrdenSenas(Number.isNaN(numero) ? undefined : numero);
  const createOrdenSena = useCreateOrdenSena();
  const updateOrden = useUpdateOrden();
  const deleteOrden = useDeleteOrden();
  const navigate = useNavigate();
  const [editando, setEditando] = useState(false);
  const [proveedorSeleccionado, setProveedorSeleccionado] = useState("");
  const [montoSena, setMontoSena] = useState("");
  const [errorSena, setErrorSena] = useState<string | null>(null);

  const totalSenas =
    orden?.total_senas ?? orden?.sena ?? 0;
  const restoPagar =
    orden && orden.costo_estimado !== null && orden.costo_estimado !== undefined
      ? orden.resto_pagar ?? orden.costo_estimado - totalSenas
      : null;

  const {
    register,
    handleSubmit,
    reset,
    setError,
    clearErrors,
    setValue,
    formState: { errors }
  } = useForm<OrdenUpdateFormValues>({
    resolver: zodResolver(ordenUpdateFormSchema),
    defaultValues: {
      estado: "",
      fecha_retiro: "",
      problema: "",
      diagnostico: "",
      costo_estimado: "",
      costo_bruto: "",
      costo_revision: "",
      costo_final: "",
      proveedor: "",
      sena_revision: "",
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
      costo_bruto:
        orden.costo_bruto !== null && orden.costo_bruto !== undefined
          ? String(orden.costo_bruto)
          : "",
      costo_revision:
        orden.costo_revision !== null && orden.costo_revision !== undefined
          ? String(orden.costo_revision)
          : "",
      costo_final:
        orden.costo_final !== null && orden.costo_final !== undefined
          ? String(orden.costo_final)
          : "",
      proveedor: orden.proveedor ?? "",
      sena_revision:
        orden.sena_revision !== null && orden.sena_revision !== undefined
          ? String(orden.sena_revision)
          : "",
      notas: orden.notas ?? ""
    });
    if (orden.proveedor && proveedores.includes(orden.proveedor)) {
      setProveedorSeleccionado(orden.proveedor);
    } else if (orden.proveedor) {
      setProveedorSeleccionado("Otros...");
    } else {
      setProveedorSeleccionado("");
    }
  }, [orden, reset]);

  const onSubmit = async (values: OrdenUpdateFormValues) => {
    if (!orden) return;
    const payload: OrdenUpdatePayload = {
      numero_orden: orden.numero_orden
    };

    const proveedorFinal =
      proveedorSeleccionado === "Otros..."
        ? values.proveedor?.trim()
        : proveedorSeleccionado || "";
    if (proveedorSeleccionado === "Otros..." && !proveedorFinal) {
      setError("proveedor", { type: "manual", message: "Proveedor requerido" });
      return;
    }

    if (values.estado) payload.estado = values.estado as OrdenEstado;
    if (values.fecha_retiro) payload.fecha_retiro = values.fecha_retiro;
    if (values.problema) payload.problema = values.problema;
    if (values.diagnostico) payload.diagnostico = values.diagnostico;
    if (values.costo_estimado) payload.costo_estimado = Number(values.costo_estimado);
    if (values.costo_bruto) payload.costo_bruto = Number(values.costo_bruto);
    if (values.costo_revision) payload.costo_revision = Number(values.costo_revision);
    if (values.costo_final) payload.costo_final = Number(values.costo_final);
    if (proveedorFinal) payload.proveedor = proveedorFinal;
    if (values.sena_revision) payload.sena_revision = Number(values.sena_revision);
    if (values.notas) payload.notas = values.notas;

    await updateOrden.mutateAsync(payload);
    setEditando(false);
  };

  const actualizarEstado = async (estado: OrdenEstado) => {
    if (!orden) return;
    await updateOrden.mutateAsync({
      numero_orden: orden.numero_orden,
      estado
    });
  };

  const marcarLista = async () => {
    await actualizarEstado("LISTA");
    if (!cliente?.telefono_contacto) return;
    const confirmar = window.confirm("Avisar telefono listo por WhatsApp?");
    if (!confirmar) return;
    const soloDigitos = cliente.telefono_contacto.replace(/\D/g, "");
    if (!soloDigitos) return;
    let telefono = soloDigitos;
    if (!telefono.startsWith("549")) {
      telefono = telefono.startsWith("54")
        ? `549${telefono.slice(2)}`
        : `549${telefono}`;
    }
    const url =
      `https://wa.me/${telefono}?text=Su%20tel%C3%A9fono%20ya%20est%C3%A1%20reparado.`;
    window.open(url, "_blank", "noopener,noreferrer");
  };

  const marcarEnProceso = async () => {
    await actualizarEstado("EN_PROCESO");
  };

  const cerrarOrden = async () => {
    if (!orden) return;
    const fecha = new Date().toISOString().slice(0, 10);
    await updateOrden.mutateAsync({
      numero_orden: orden.numero_orden,
      estado: "CERRADA",
      fecha_retiro: fecha
    });
  };

  const imprimirComprobante = () => {
    if (!orden || USE_MOCKS || !API_BASE) return;
    const url = `${API_BASE}/ordenes_trabajo/${orden.numero_orden}/comprobante.pdf`;
    window.open(url, "_blank", "noopener,noreferrer");
  };

  const agregarSena = async () => {
    if (!orden) return;
    const monto = Number(montoSena);
    if (!montoSena || Number.isNaN(monto) || monto <= 0) {
      setErrorSena("Ingresa un monto valido.");
      return;
    }
    setErrorSena(null);
    const payload: OrdenSenaCreatePayload = { monto };
    await createOrdenSena.mutateAsync({
      numero: orden.numero_orden,
      payload
    });
    setMontoSena("");
  };

  const eliminarOrden = async () => {
    if (!orden) return;
    const confirmado = window.confirm(
      "Eliminar orden? Esto no se puede deshacer."
    );
    if (!confirmado) return;
    try {
      await deleteOrden.mutateAsync(orden.numero_orden);
      navigate("/ordenes");
    } catch (_error) {
      window.alert("No se pudo eliminar la orden.");
    }
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
                <span>Costo bruto</span>
                <span className="font-semibold text-ink">
                  ${orden.costo_bruto ?? "-"}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span>Total senas</span>
                <span className="font-semibold text-ink">
                  ${totalSenas}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span>Resto a pagar</span>
                <span className="font-semibold text-ink">
                  ${restoPagar ?? "-"}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span>Costo revision</span>
                <span className="font-semibold text-ink">
                  ${orden.costo_revision ?? "-"}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span>Sena revision</span>
                <span className="font-semibold text-ink">
                  ${orden.sena_revision ?? "-"}
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
              <Button
                variant="secondary"
                type="button"
                disabled={
                  updateOrden.isPending ||
                  orden.estado === "EN_PROCESO" ||
                  orden.estado === "CERRADA" ||
                  orden.estado === "CANCELADA"
                }
                onClick={marcarEnProceso}
              >
                Marcar en proceso
              </Button>
              <Button
                variant="outline"
                type="button"
                disabled={
                  updateOrden.isPending ||
                  orden.estado === "LISTA" ||
                  orden.estado === "CERRADA" ||
                  orden.estado === "CANCELADA"
                }
                onClick={marcarLista}
              >
                Listo para retiro
              </Button>
              <Button
                variant="ghost"
                type="button"
                disabled={
                  updateOrden.isPending ||
                  orden.estado === "CERRADA" ||
                  orden.estado === "CANCELADA"
                }
                onClick={cerrarOrden}
              >
                Cerrar orden
              </Button>
              <Button type="button" onClick={() => setEditando((prev) => !prev)}>
                {editando ? "Cancelar edicion" : "Editar orden"}
              </Button>
              <Button
                type="button"
                variant="outline"
                onClick={imprimirComprobante}
                disabled={USE_MOCKS || !orden}
              >
                Imprimir comprobante
              </Button>
              <Button
                type="button"
                variant="outline"
                onClick={eliminarOrden}
                disabled={deleteOrden.isPending || !orden}
                className="border-ember/40 text-ember hover:bg-ember/10"
              >
                Eliminar orden
              </Button>
            </div>
          </Card>
        </div>
      ) : null}

      {orden ? (
        <Card>
          <CardHeader>
            <CardTitle>Senas</CardTitle>
          </CardHeader>
          <div className="flex flex-col gap-4">
            <div className="flex flex-col gap-2 sm:flex-row sm:items-end">
              <div className="flex-1">
                <label className="text-sm font-semibold">Agregar sena</label>
                <Input
                  placeholder="2000"
                  value={montoSena}
                  onChange={(event) => {
                    setMontoSena(event.target.value);
                    setErrorSena(null);
                  }}
                />
                {errorSena ? (
                  <p className="mt-1 text-xs text-ember">{errorSena}</p>
                ) : null}
              </div>
              <Button
                type="button"
                onClick={agregarSena}
                disabled={createOrdenSena.isPending}
              >
                {createOrdenSena.isPending ? "Guardando..." : "Agregar sena"}
              </Button>
            </div>

            <div className="divide-y divide-ink/10 rounded-2xl border border-ink/10">
              {senas.length === 0 ? (
                <div className="px-4 py-6 text-sm text-ink/60">
                  Aun no hay senas cargadas.
                </div>
              ) : null}
              {senas.map((sena) => (
                <div
                  key={sena.id}
                  className="flex items-center justify-between px-4 py-3 text-sm text-ink/70"
                >
                  <span>
                    {format(parseISO(sena.created_at), "dd/MM/yyyy")}
                  </span>
                  <span className="font-semibold text-ink">${sena.monto}</span>
                </div>
              ))}
            </div>
          </div>
        </Card>
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
                <label className="text-sm font-semibold">Costo bruto</label>
                <Input placeholder="40000" {...register("costo_bruto")} />
                {errors.costo_bruto ? (
                  <p className="mt-1 text-xs text-ember">
                    {errors.costo_bruto.message}
                  </p>
                ) : null}
              </div>
            </div>

            <div className="grid gap-4 md:grid-cols-2">
              <div>
                <label className="text-sm font-semibold">Costo revision</label>
                <Input placeholder="3000" {...register("costo_revision")} />
                {errors.costo_revision ? (
                  <p className="mt-1 text-xs text-ember">
                    {errors.costo_revision.message}
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
                <Select
                  value={proveedorSeleccionado}
                  onChange={(event) => {
                    setProveedorSeleccionado(event.target.value);
                    if (event.target.value !== "Otros...") {
                      setValue("proveedor", "");
                      clearErrors("proveedor");
                    }
                  }}
                >
                  <option value="">Seleccionar proveedor</option>
                  {proveedores.map((proveedor) => (
                    <option key={proveedor} value={proveedor}>
                      {proveedor}
                    </option>
                  ))}
                </Select>
                {proveedorSeleccionado === "Otros..." ? (
                  <div className="mt-3">
                    <Input
                      placeholder="Proveedor"
                      {...register("proveedor", {
                        onChange: () => clearErrors("proveedor")
                      })}
                    />
                  </div>
                ) : null}
                {proveedorSeleccionado === "Otros..." && errors.proveedor ? (
                  <p className="mt-1 text-xs text-ember">
                    {errors.proveedor.message}
                  </p>
                ) : null}
              </div>
              <div>
                <label className="text-sm font-semibold">Sena revision</label>
                <Input placeholder="1500" {...register("sena_revision")} />
                {errors.sena_revision ? (
                  <p className="mt-1 text-xs text-ember">
                    {errors.sena_revision.message}
                  </p>
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
