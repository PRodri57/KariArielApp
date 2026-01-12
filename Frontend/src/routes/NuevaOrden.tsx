import { useEffect, useMemo, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { Button } from "@/components/ui/Button";
import { Card, CardDescription, CardHeader, CardTitle } from "@/components/ui/Card";
import { Input } from "@/components/ui/Input";
import { Select } from "@/components/ui/Select";
import { Textarea } from "@/components/ui/Textarea";
import { useClientes } from "@/hooks/clientes";
import { useCreateOrden } from "@/hooks/ordenes";
import { useTelefonos } from "@/hooks/telefonos";
import { ordenFormSchema, type OrdenFormValues } from "@/lib/validation";

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

export function NuevaOrden() {
  const [numeroCreado, setNumeroCreado] = useState<number | null>(null);
  const [errorMensaje, setErrorMensaje] = useState<string | null>(null);
  const [dniBusqueda, setDniBusqueda] = useState("");
  const [dniEncontrado, setDniEncontrado] = useState<null | "encontrado" | "no-encontrado">(null);
  const [proveedorSeleccionado, setProveedorSeleccionado] = useState("");
  const [searchParams] = useSearchParams();
  const { data: clientes = [] } = useClientes();
  const { data: telefonos = [] } = useTelefonos();
  const createOrden = useCreateOrden();
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
    clearErrors,
    setError,
    setValue,
    watch
  } = useForm<OrdenFormValues>({
    resolver: zodResolver(ordenFormSchema),
    defaultValues: {
      cliente_id: "",
      telefono_id: "",
      problema: "",
      diagnostico: "",
      costo_estimado: "",
      costo_bruto: "",
      costo_revision: "",
      proveedor: "",
      sena: "",
      notas: ""
    }
  });

  const clienteSeleccionado = watch("cliente_id");
  const telefonoSeleccionado = watch("telefono_id");
  const telefonosFiltrados = useMemo(() => {
    const id = Number(clienteSeleccionado);
    if (!id) return [];
    return telefonos.filter((telefono) => telefono.cliente_id === id);
  }, [clienteSeleccionado, telefonos]);

  useEffect(() => {
    const telefonoId = Number(searchParams.get("telefono_id") ?? "");
    if (!telefonoId) return;
    const telefono = telefonos.find((item) => item.id === telefonoId);
    if (!telefono) return;
    setValue("cliente_id", String(telefono.cliente_id));
    setValue("telefono_id", String(telefonoId));
  }, [searchParams, setValue, telefonos]);

  useEffect(() => {
    if (!clienteSeleccionado) {
      setValue("telefono_id", "");
      return;
    }
    const existe = telefonosFiltrados.some(
      (telefono) => String(telefono.id) === telefonoSeleccionado
    );
    if (!existe) {
      setValue("telefono_id", "");
    }
  }, [clienteSeleccionado, telefonoSeleccionado, telefonosFiltrados, setValue]);

  const onSubmit = async (values: OrdenFormValues) => {
    setErrorMensaje(null);
    setNumeroCreado(null);
    const payload = {
      telefono_id: Number(values.telefono_id),
      problema: values.problema,
      diagnostico: values.diagnostico || undefined,
      costo_estimado: values.costo_estimado
        ? Number(values.costo_estimado)
        : undefined,
      costo_bruto: values.costo_bruto ? Number(values.costo_bruto) : undefined,
      costo_revision: values.costo_revision
        ? Number(values.costo_revision)
        : undefined,
      proveedor:
        proveedorSeleccionado === "Otros..."
          ? values.proveedor?.trim() || undefined
          : proveedorSeleccionado || undefined,
      sena: values.sena ? Number(values.sena) : undefined,
      notas: values.notas || undefined
    };

    if (proveedorSeleccionado === "Otros..." && !payload.proveedor) {
      setError("proveedor", {
        type: "manual",
        message: "Proveedor requerido"
      });
      return;
    }

    try {
      const result = await createOrden.mutateAsync(payload);
      setNumeroCreado(result.numero_orden);
      reset({
        cliente_id: values.cliente_id,
        telefono_id: "",
        problema: "",
        diagnostico: "",
        costo_estimado: "",
      costo_bruto: "",
      costo_revision: "",
      proveedor: "",
      sena: "",
      notas: ""
    });
      setProveedorSeleccionado("");
    } catch (error) {
      const message =
        error instanceof Error ? error.message : "No se pudo crear la orden.";
      setErrorMensaje(message);
    }
  };

  const buscarPorDni = () => {
    const dni = dniBusqueda.trim();
    if (!dni) {
      setDniEncontrado(null);
      return;
    }
    const cliente = clientes.find((item) => item.dni === dni);
    if (cliente) {
      setValue("cliente_id", String(cliente.id));
      setDniEncontrado("encontrado");
    } else {
      setDniEncontrado("no-encontrado");
    }
  };

  return (
    <div className="flex flex-col gap-6">
      <Card>
        <CardHeader>
          <CardTitle>Nueva orden</CardTitle>
          <CardDescription>Selecciona cliente, equipo y guarda.</CardDescription>
        </CardHeader>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          {errorMensaje ? (
            <div className="rounded-2xl border border-ember/20 bg-ember/10 px-4 py-3 text-sm text-ember">
              {errorMensaje}
            </div>
          ) : null}
          <div className="rounded-2xl border border-ink/10 bg-ink/5 px-4 py-3">
            <label className="text-sm font-semibold">Buscar cliente por DNI</label>
            <div className="mt-2 flex flex-col gap-2 md:flex-row md:items-center">
              <Input
                placeholder="Ingresar DNI"
                value={dniBusqueda}
                onChange={(event) => {
                  setDniBusqueda(event.target.value);
                  setDniEncontrado(null);
                }}
                onBlur={buscarPorDni}
              />
              <Button type="button" variant="outline" onClick={buscarPorDni}>
                Buscar
              </Button>
            </div>
            {dniEncontrado === "encontrado" ? (
              <p className="mt-2 text-xs text-moss">Cliente encontrado y seleccionado.</p>
            ) : null}
            {dniEncontrado === "no-encontrado" ? (
              <div className="mt-2 flex flex-wrap items-center gap-2 text-xs text-ember">
                <span>No existe cliente con ese DNI. Queres crear uno nuevo?</span>
                <Link to="/clientes/nuevo" className="underline">
                  Crear cliente
                </Link>
              </div>
            ) : null}
          </div>

          <div className="grid gap-4 md:grid-cols-2">
            <div>
              <label className="text-sm font-semibold">Cliente</label>
              <Select {...register("cliente_id")}>
                <option value="">Selecciona un cliente</option>
                {clientes.map((cliente) => (
                  <option key={cliente.id} value={cliente.id}>
                    {cliente.nombre}
                  </option>
                ))}
              </Select>
              {errors.cliente_id ? (
                <p className="mt-1 text-xs text-ember">
                  {errors.cliente_id.message}
                </p>
              ) : null}
            </div>

            <div>
              <label className="text-sm font-semibold">Telefono</label>
              <Select
                {...register("telefono_id")}
                disabled={!clienteSeleccionado}
              >
                <option value="">
                  {clienteSeleccionado
                    ? "Selecciona un telefono"
                    : "Primero elige un cliente"}
                </option>
                {telefonosFiltrados.map((telefono) => (
                  <option key={telefono.id} value={telefono.id}>
                    {telefono.marca} {telefono.modelo}
                  </option>
                ))}
              </Select>
              {errors.telefono_id ? (
                <p className="mt-1 text-xs text-ember">
                  {errors.telefono_id.message}
                </p>
              ) : null}
            </div>
          </div>

          {clientes.length === 0 ? (
            <div className="rounded-2xl border border-ink/10 bg-ink/5 px-4 py-3 text-sm text-ink/70">
              No hay clientes cargados.{" "}
              <Link to="/clientes/nuevo" className="underline">
                Crear cliente
              </Link>
            </div>
          ) : null}

          {clienteSeleccionado && telefonosFiltrados.length === 0 ? (
            <div className="rounded-2xl border border-ink/10 bg-ink/5 px-4 py-3 text-sm text-ink/70">
              Este cliente aun no tiene telefonos cargados.
            </div>
          ) : null}

          <div>
            <label className="text-sm font-semibold">Problema reportado</label>
            <Textarea
              placeholder="Pantalla rota, no enciende, bateria dura poco..."
              {...register("problema")}
            />
            {errors.problema ? (
              <p className="mt-1 text-xs text-ember">{errors.problema.message}</p>
            ) : null}
          </div>

          <div>
            <label className="text-sm font-semibold">Diagnostico</label>
            <Textarea
              placeholder="Se revisa flex, se detecta humedad..."
              {...register("diagnostico")}
            />
          </div>

          <div className="grid gap-4 md:grid-cols-2">
            <div>
              <label className="text-sm font-semibold">Presupuesto</label>
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
                  <p className="mt-1 text-xs text-ember">{errors.proveedor.message}</p>
                ) : null}
            </div>
            <div>
              <label className="text-sm font-semibold">Costo revision</label>
              <Input placeholder="3000" {...register("costo_revision")} />
              {errors.costo_revision ? (
                <p className="mt-1 text-xs text-ember">
                  {errors.costo_revision.message}
                </p>
              ) : null}
            </div>
          </div>

          <div>
            <label className="text-sm font-semibold">Sena</label>
            <Input placeholder="5000" {...register("sena")} />
            {errors.sena ? (
              <p className="mt-1 text-xs text-ember">{errors.sena.message}</p>
            ) : null}
          </div>

          <div>
            <label className="text-sm font-semibold">Notas internas</label>
            <Input placeholder="Urgente, repuesto en camino" {...register("notas")} />
          </div>

          <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
            <Button type="submit" size="lg" disabled={createOrden.isPending}>
              {createOrden.isPending ? "Creando..." : "Crear orden"}
            </Button>
            {numeroCreado ? (
              <div className="rounded-2xl border border-ember/20 bg-ember/10 px-4 py-3 text-sm text-ember">
                Orden creada: #{numeroCreado}
              </div>
            ) : null}
          </div>
        </form>
      </Card>
    </div>
  );
}
