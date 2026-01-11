import { useEffect, useMemo, useState } from "react";
import { format, parseISO } from "date-fns";
import { Link, useNavigate, useParams } from "react-router-dom";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { Button } from "@/components/ui/Button";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { Input } from "@/components/ui/Input";
import { Textarea } from "@/components/ui/Textarea";
import { StatusBadge } from "@/components/StatusBadge";
import { useCliente, useDeleteCliente } from "@/hooks/clientes";
import { useOrdenes } from "@/hooks/ordenes";
import { useCreateTelefono, useTelefonos, useUpdateTelefono } from "@/hooks/telefonos";
import { telefonoFormSchema, type TelefonoFormValues } from "@/lib/validation";

export function ClienteDetalle() {
  const params = useParams();
  const clienteId = Number(params.id);
  const idValido = !Number.isNaN(clienteId);

  const { data: cliente, isLoading } = useCliente(idValido ? clienteId : undefined);
  const deleteCliente = useDeleteCliente();
  const navigate = useNavigate();
  const { data: telefonos = [], isLoading: telefonosLoading } = useTelefonos(
    idValido ? clienteId : undefined
  );
  const { data: ordenes = [], isLoading: ordenesLoading } = useOrdenes();
  const createTelefono = useCreateTelefono();
  const updateTelefono = useUpdateTelefono();

  const telefonoLabelMap = useMemo(() => {
    const map = new Map<number, string>();
    telefonos.forEach((telefono) => {
      map.set(telefono.id, `${telefono.marca} ${telefono.modelo}`);
    });
    return map;
  }, [telefonos]);

  const ordenesCliente = useMemo(() => {
    const ids = new Set(telefonos.map((telefono) => telefono.id));
    return ordenes.filter(
      (orden) => ids.has(orden.telefono_id) || orden.cliente_id === clienteId
    );
  }, [ordenes, telefonos, clienteId]);

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
    setValue
  } = useForm<TelefonoFormValues>({
    resolver: zodResolver(telefonoFormSchema),
    defaultValues: {
      cliente_id: idValido ? String(clienteId) : "",
      marca: "",
      modelo: "",
      notas: ""
    }
  });

  useEffect(() => {
    if (idValido) {
      setValue("cliente_id", String(clienteId));
    }
  }, [clienteId, idValido, setValue]);

  const onSubmit = async (values: TelefonoFormValues) => {
    if (!idValido) return;
    const payload = {
      cliente_id: clienteId,
      marca: values.marca,
      modelo: values.modelo,
      notas: values.notas || undefined
    };

    await createTelefono.mutateAsync(payload);
    reset({
      cliente_id: String(clienteId),
      marca: "",
      modelo: "",
      notas: ""
    });
  };

  const [editandoTelefono, setEditandoTelefono] = useState<number | null>(null);
  const {
    register: registerEdit,
    handleSubmit: handleSubmitEdit,
    formState: { errors: editErrors },
    reset: resetEdit
  } = useForm<TelefonoFormValues>({
    resolver: zodResolver(telefonoFormSchema),
    defaultValues: {
      cliente_id: idValido ? String(clienteId) : "",
      marca: "",
      modelo: "",
      notas: ""
    }
  });

  const iniciarEdicion = (telefonoId: number) => {
    const telefono = telefonos.find((item) => item.id === telefonoId);
    if (!telefono) return;
    resetEdit({
      cliente_id: String(telefono.cliente_id),
      marca: telefono.marca,
      modelo: telefono.modelo,
      notas: telefono.notas ?? ""
    });
    setEditandoTelefono(telefonoId);
  };

  const cancelarEdicion = () => {
    setEditandoTelefono(null);
  };

  const onSubmitEdit = async (values: TelefonoFormValues) => {
    if (!editandoTelefono) return;
    await updateTelefono.mutateAsync({
      id: editandoTelefono,
      marca: values.marca,
      modelo: values.modelo,
      notas: values.notas || undefined
    });
    setEditandoTelefono(null);
  };

  const eliminarCliente = async () => {
    if (!cliente) return;
    const confirmado = window.confirm(
      "Eliminar cliente? Esto no se puede deshacer."
    );
    if (!confirmado) return;
    try {
      await deleteCliente.mutateAsync(cliente.id);
      navigate("/clientes");
    } catch (_error) {
      window.alert("No se pudo eliminar el cliente.");
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div>
          <p className="text-xs uppercase tracking-[0.3em] text-ink/50">Cliente</p>
          <h2 className="text-3xl">
            {cliente?.nombre ?? (isLoading ? "Cargando..." : "No encontrado")}
          </h2>
        </div>
        <div className="flex flex-wrap items-center gap-2">
          <Link to="/clientes">
            <Button variant="outline">Volver a clientes</Button>
          </Link>
          <Button
            type="button"
            variant="outline"
            onClick={eliminarCliente}
            disabled={deleteCliente.isPending || !cliente}
            className="border-ember/40 text-ember hover:bg-ember/10"
          >
            Eliminar cliente
          </Button>
        </div>
      </div>

      {!idValido ? (
        <Card>
          <p className="text-sm text-ink/60">Cliente no valido.</p>
        </Card>
      ) : null}

      {idValido && !isLoading && !cliente ? (
        <Card>
          <p className="text-sm text-ink/60">No se encontro el cliente.</p>
        </Card>
      ) : null}

      {cliente ? (
        <div className="grid gap-6 lg:grid-cols-[2fr_1fr]">
          <div className="flex flex-col gap-6">
            <Card>
              <CardHeader>
                <CardTitle>Datos</CardTitle>
              </CardHeader>
              <div className="grid gap-4 text-sm text-ink/70">
                <div className="flex items-center justify-between">
                  <span>DNI</span>
                  <span className="font-semibold text-ink">
                    {cliente.dni ?? "-"}
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span>Contacto</span>
                  <span className="font-semibold text-ink">
                    {cliente.telefono_contacto ?? "-"}
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span>Email</span>
                  <span className="font-semibold text-ink">
                    {cliente.email ?? "-"}
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span>Alta</span>
                  <span className="font-semibold text-ink">
                    {format(parseISO(cliente.creado_en), "dd MMM yyyy")}
                  </span>
                </div>
                {cliente.notas ? (
                  <div className="rounded-2xl border border-ink/10 bg-ink/5 px-4 py-3 text-sm text-ink/70">
                    {cliente.notas}
                  </div>
                ) : null}
              </div>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Telefonos</CardTitle>
              </CardHeader>
              <div className="flex flex-col gap-4">
                {telefonosLoading ? (
                  <p className="text-sm text-ink/60">Cargando...</p>
                ) : null}
                {!telefonosLoading && telefonos.length === 0 ? (
                  <p className="text-sm text-ink/60">
                    Aun no hay telefonos cargados.
                  </p>
                ) : null}
                {telefonos.map((telefono) => (
                  <div
                    key={telefono.id}
                    className="flex flex-col gap-3 rounded-2xl border border-ink/10 bg-ink/5 px-4 py-3 text-sm text-ink/70"
                  >
                    {editandoTelefono === telefono.id ? (
                      <form
                        onSubmit={handleSubmitEdit(onSubmitEdit)}
                        className="grid gap-3 md:grid-cols-[1fr_1fr_auto]"
                      >
                        <input type="hidden" {...registerEdit("cliente_id")} />
                        <div>
                          <label className="text-xs font-semibold">Marca</label>
                          <Input placeholder="Samsung" {...registerEdit("marca")} />
                          {editErrors.marca ? (
                            <p className="mt-1 text-xs text-ember">
                              {editErrors.marca.message}
                            </p>
                          ) : null}
                        </div>
                        <div>
                          <label className="text-xs font-semibold">Modelo</label>
                          <Input placeholder="A52" {...registerEdit("modelo")} />
                          {editErrors.modelo ? (
                            <p className="mt-1 text-xs text-ember">
                              {editErrors.modelo.message}
                            </p>
                          ) : null}
                        </div>
                        <div className="flex items-end gap-2">
                          <Button type="submit" size="sm">
                            Guardar
                          </Button>
                          <Button
                            type="button"
                            size="sm"
                            variant="ghost"
                            onClick={cancelarEdicion}
                          >
                            Cancelar
                          </Button>
                        </div>
                        <div className="md:col-span-3">
                          <label className="text-xs font-semibold">Notas</label>
                          <Textarea
                            placeholder="Detalle de equipo, repuestos..."
                            {...registerEdit("notas")}
                          />
                        </div>
                      </form>
                    ) : (
                      <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
                        <div>
                          <p className="font-semibold text-ink">
                            {telefono.marca} {telefono.modelo}
                          </p>
                          {telefono.notas ? (
                            <p className="text-xs text-ink/50">{telefono.notas}</p>
                          ) : null}
                        </div>
                        <div className="flex flex-wrap gap-2">
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() => iniciarEdicion(telefono.id)}
                          >
                            Editar
                          </Button>
                          <Link to={`/ordenes/nueva?telefono_id=${telefono.id}`}>
                            <Button size="sm" variant="outline">
                              Nueva orden
                            </Button>
                          </Link>
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </Card>

            <Card className="overflow-hidden p-0">
              <div className="grid grid-cols-4 gap-2 border-b border-ink/10 bg-haze/70 px-6 py-4 text-xs uppercase tracking-[0.3em] text-ink/40">
                <span>Orden</span>
                <span>Equipo</span>
                <span>Estado</span>
                <span>Ingreso</span>
              </div>
              <div className="divide-y divide-ink/10">
                {ordenesLoading ? (
                  <div className="px-6 py-8 text-sm text-ink/60">
                    Cargando...
                  </div>
                ) : null}
                {!ordenesLoading && ordenesCliente.length === 0 ? (
                  <div className="px-6 py-8 text-sm text-ink/60">
                    No hay ordenes para este cliente.
                  </div>
                ) : null}
                {ordenesCliente.map((orden) => (
                  <Link
                    key={orden.numero_orden}
                    to={`/ordenes/${orden.numero_orden}`}
                    className="grid grid-cols-1 gap-2 px-6 py-4 text-sm transition hover:bg-ink/5 md:grid-cols-4"
                  >
                    <span className="font-semibold text-ink">
                      #{orden.numero_orden}
                    </span>
                    <span className="text-ink/70">
                      {orden.telefono_label ??
                        telefonoLabelMap.get(orden.telefono_id) ??
                        `Telefono #${orden.telefono_id}`}
                    </span>
                    <StatusBadge estado={orden.estado} />
                    <span className="text-ink/60">
                      {format(parseISO(orden.fecha_ingreso), "dd/MM/yyyy")}
                    </span>
                  </Link>
                ))}
              </div>
            </Card>
          </div>

          <Card>
            <CardHeader>
              <CardTitle>Agregar telefono</CardTitle>
            </CardHeader>
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
              <input type="hidden" {...register("cliente_id")} />
              <div>
                <label className="text-sm font-semibold">Marca</label>
                <Input placeholder="Samsung" {...register("marca")} />
                {errors.marca ? (
                  <p className="mt-1 text-xs text-ember">{errors.marca.message}</p>
                ) : null}
              </div>
              <div>
                <label className="text-sm font-semibold">Modelo</label>
                <Input placeholder="A52" {...register("modelo")} />
                {errors.modelo ? (
                  <p className="mt-1 text-xs text-ember">{errors.modelo.message}</p>
                ) : null}
              </div>
              <div>
                <label className="text-sm font-semibold">Notas</label>
                <Textarea
                  placeholder="Detalle de equipo, repuestos..."
                  {...register("notas")}
                />
              </div>
              <Button type="submit" disabled={createTelefono.isPending}>
                {createTelefono.isPending ? "Guardando..." : "Agregar telefono"}
              </Button>
            </form>
          </Card>
        </div>
      ) : null}
    </div>
  );
}
