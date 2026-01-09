import { useState } from "react";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { Button } from "@/components/ui/Button";
import { Card, CardDescription, CardHeader, CardTitle } from "@/components/ui/Card";
import { Input } from "@/components/ui/Input";
import { Textarea } from "@/components/ui/Textarea";
import { useCreateOrden } from "@/hooks/ordenes";
import { ordenFormSchema, type OrdenFormValues } from "@/lib/validation";

export function NuevaOrden() {
  const [numeroCreado, setNumeroCreado] = useState<number | null>(null);
  const createOrden = useCreateOrden();

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset
  } = useForm<OrdenFormValues>({
    resolver: zodResolver(ordenFormSchema),
    defaultValues: {
      cliente: "",
      telefono_marca: "",
      telefono_modelo: "",
      telefono_imei: "",
      problema: "",
      diagnostico: "",
      costo_estimado: "",
      notas: ""
    }
  });

  const onSubmit = async (values: OrdenFormValues) => {
    const payload = {
      ...values,
      telefono_imei: values.telefono_imei || undefined,
      costo_estimado: values.costo_estimado
        ? Number(values.costo_estimado)
        : undefined
    };

    const result = await createOrden.mutateAsync(payload);
    setNumeroCreado(result.numero_orden);
    reset();
  };

  return (
    <div className="flex flex-col gap-6">
      <Card>
        <CardHeader>
          <CardTitle>Nueva orden</CardTitle>
          <CardDescription>Completa datos y guarda.</CardDescription>
        </CardHeader>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          <div>
            <label className="text-sm font-semibold">Cliente</label>
            <Input placeholder="Nombre y apellido" {...register("cliente")} />
            {errors.cliente ? (
              <p className="mt-1 text-xs text-ember">{errors.cliente.message}</p>
            ) : null}
          </div>

          <div className="grid gap-4 md:grid-cols-3">
            <div>
              <label className="text-sm font-semibold">Marca</label>
              <Input placeholder="Samsung" {...register("telefono_marca")} />
              {errors.telefono_marca ? (
                <p className="mt-1 text-xs text-ember">
                  {errors.telefono_marca.message}
                </p>
              ) : null}
            </div>
            <div>
              <label className="text-sm font-semibold">Modelo</label>
              <Input placeholder="A52" {...register("telefono_modelo")} />
              {errors.telefono_modelo ? (
                <p className="mt-1 text-xs text-ember">
                  {errors.telefono_modelo.message}
                </p>
              ) : null}
            </div>
            <div>
              <label className="text-sm font-semibold">IMEI</label>
              <Input placeholder="Opcional" {...register("telefono_imei")} />
              {errors.telefono_imei ? (
                <p className="mt-1 text-xs text-ember">
                  {errors.telefono_imei.message}
                </p>
              ) : null}
            </div>
          </div>

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
              <label className="text-sm font-semibold">Costo estimado</label>
              <Input placeholder="15000" {...register("costo_estimado")} />
              {errors.costo_estimado ? (
                <p className="mt-1 text-xs text-ember">
                  {errors.costo_estimado.message}
                </p>
              ) : null}
            </div>
            <div>
              <label className="text-sm font-semibold">Notas internas</label>
              <Input placeholder="Urgente, repuesto en camino" {...register("notas")} />
            </div>
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
