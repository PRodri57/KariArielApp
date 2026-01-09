import { z } from "zod";

export const ordenFormSchema = z.object({
  cliente: z.string().min(2, "Nombre requerido"),
  telefono_marca: z.string().min(2, "Marca requerida"),
  telefono_modelo: z.string().min(1, "Modelo requerido"),
  telefono_imei: z
    .string()
    .optional()
    .refine(
      (value) => !value || /^[0-9]{14,16}$/.test(value),
      "IMEI invalido"
    ),
  problema: z.string().min(10, "Describe mejor el problema"),
  diagnostico: z.string().optional(),
  costo_estimado: z
    .string()
    .optional()
    .refine(
      (value) => !value || /^\d+(\.\d{1,2})?$/.test(value),
      "Costo invalido"
    ),
  notas: z.string().optional()
});

export type OrdenFormValues = z.infer<typeof ordenFormSchema>;
