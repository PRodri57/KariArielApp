import { Badge } from "@/components/ui/Badge";
import type { OrdenEstado } from "@/lib/types";

const statusMap: Record<OrdenEstado, { label: string; variant: "info" | "success" | "warning" | "neutral" }> = {
  ABIERTA: { label: "Abierta", variant: "warning" },
  EN_PROCESO: { label: "En proceso", variant: "info" },
  ESPERANDO_REPUESTO: { label: "Esperando repuesto", variant: "neutral" },
  LISTA: { label: "Lista", variant: "success" },
  CERRADA: { label: "Cerrada", variant: "neutral" },
  CANCELADA: { label: "Cancelada", variant: "neutral" }
};

export function StatusBadge({ estado }: { estado: OrdenEstado }) {
  const { label, variant } = statusMap[estado];
  return <Badge variant={variant}>{label}</Badge>;
}
