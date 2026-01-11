import { z } from "zod";

export const ordenFormSchema = z.object({
  cliente_id: z.string().min(1, "Cliente requerido"),
  telefono_id: z.string().min(1, "Telefono requerido"),
  problema: z.string().min(10, "Describe mejor el problema"),
  diagnostico: z.string().optional(),
  costo_estimado: z
    .string()
    .optional()
    .refine(
      (value) => !value || /^\d+(\.\d{1,2})?$/.test(value),
      "Costo invalido"
    ),
  proveedor: z.string().optional(),
  sena: z
    .string()
    .optional()
    .refine(
      (value) => !value || /^\d+(\.\d{1,2})?$/.test(value),
      "Sena invalida"
    ),
  notas: z.string().optional()
});

export type OrdenFormValues = z.infer<typeof ordenFormSchema>;

export const ordenUpdateFormSchema = z.object({
  estado: z.string().optional(),
  fecha_retiro: z
    .string()
    .optional()
    .refine(
      (value) => !value || /^\d{4}-\d{2}-\d{2}$/.test(value),
      "Fecha invalida"
    ),
  problema: z.string().optional(),
  diagnostico: z.string().optional(),
  costo_estimado: z
    .string()
    .optional()
    .refine(
      (value) => !value || /^\d+(\.\d{1,2})?$/.test(value),
      "Costo invalido"
    ),
  costo_final: z
    .string()
    .optional()
    .refine(
      (value) => !value || /^\d+(\.\d{1,2})?$/.test(value),
      "Costo invalido"
    ),
  proveedor: z.string().optional(),
  sena: z
    .string()
    .optional()
    .refine(
      (value) => !value || /^\d+(\.\d{1,2})?$/.test(value),
      "Sena invalida"
    ),
  notas: z.string().optional()
});

export type OrdenUpdateFormValues = z.infer<typeof ordenUpdateFormSchema>;

export const clienteFormSchema = z.object({
  nombre: z.string().min(2, "Nombre requerido"),
  dni: z
    .string()
    .optional()
    .refine((value) => !value || /^[0-9]{6,9}$/.test(value), "DNI invalido"),
  telefono_contacto: z.string().optional(),
  notas: z.string().optional()
});

export type ClienteFormValues = z.infer<typeof clienteFormSchema>;

export const telefonoFormSchema = z.object({
  cliente_id: z.string().min(1, "Cliente requerido"),
  marca: z.string().min(2, "Marca requerida"),
  modelo: z.string().min(1, "Modelo requerido"),
  notas: z.string().optional()
});

export type TelefonoFormValues = z.infer<typeof telefonoFormSchema>;
