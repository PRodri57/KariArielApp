import { useState } from "react";
import { Link } from "react-router-dom";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { Button } from "@/components/ui/Button";
import { Card, CardDescription, CardHeader, CardTitle } from "@/components/ui/Card";
import { Input } from "@/components/ui/Input";
import { Textarea } from "@/components/ui/Textarea";
import { useCreateCliente } from "@/hooks/clientes";
import { clienteFormSchema, type ClienteFormValues } from "@/lib/validation";

export function NuevoCliente() {
  const [clienteCreado, setClienteCreado] = useState<number | null>(null);
  const createCliente = useCreateCliente();

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset
  } = useForm<ClienteFormValues>({
    resolver: zodResolver(clienteFormSchema),
    defaultValues: {
      nombre: "",
      dni: "",
      telefono_contacto: "",
      email: "",
      notas: ""
    }
  });

  const onSubmit = async (values: ClienteFormValues) => {
    const payload = {
      nombre: values.nombre,
      dni: values.dni,
      telefono_contacto: values.telefono_contacto || undefined,
      email: values.email || undefined,
      notas: values.notas || undefined
    };

    const result = await createCliente.mutateAsync(payload);
    setClienteCreado(result.id);
    reset();
  };

  return (
    <div className="flex flex-col gap-6">
      <Card>
        <CardHeader>
          <CardTitle>Nuevo cliente</CardTitle>
          <CardDescription>Carga los datos basicos del cliente.</CardDescription>
        </CardHeader>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          <div>
            <label className="text-sm font-semibold">Nombre y apellido</label>
            <Input placeholder="Juan Perez" {...register("nombre")} />
            {errors.nombre ? (
              <p className="mt-1 text-xs text-ember">{errors.nombre.message}</p>
            ) : null}
          </div>

          <div className="grid gap-4 md:grid-cols-2">
            <div>
              <label className="text-sm font-semibold">DNI / CUIL</label>
              <Input placeholder="12345678 o 20123456789" {...register("dni")} />
              {errors.dni ? (
                <p className="mt-1 text-xs text-ember">{errors.dni.message}</p>
              ) : null}
            </div>
            <div>
              <label className="text-sm font-semibold">Telefono contacto</label>
              <Input placeholder="11 5555-1234" {...register("telefono_contacto")} />
            </div>
          </div>

          <div>
            <label className="text-sm font-semibold">Email</label>
            <Input placeholder="cliente@email.com" {...register("email")} />
            {errors.email ? (
              <p className="mt-1 text-xs text-ember">{errors.email.message}</p>
            ) : null}
          </div>

          <div>
            <label className="text-sm font-semibold">Notas</label>
            <Textarea placeholder="Preferencias, horarios..." {...register("notas")} />
          </div>

          <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
            <Button type="submit" size="lg" disabled={createCliente.isPending}>
              {createCliente.isPending ? "Guardando..." : "Crear cliente"}
            </Button>
            {clienteCreado ? (
              <div className="flex items-center gap-3 rounded-2xl border border-ember/20 bg-ember/10 px-4 py-3 text-sm text-ember">
                Cliente creado: #{clienteCreado}
                <Link to={`/clientes/${clienteCreado}`} className="underline">
                  Ver ficha
                </Link>
              </div>
            ) : null}
          </div>
        </form>
      </Card>
    </div>
  );
}
