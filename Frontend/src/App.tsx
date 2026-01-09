import { Route, Routes } from "react-router-dom";
import { AppShell } from "@/components/layout/AppShell";
import { Dashboard } from "@/routes/Dashboard";
import { NuevaOrden } from "@/routes/NuevaOrden";
import { OrdenDetalle } from "@/routes/OrdenDetalle";
import { Ordenes } from "@/routes/Ordenes";
import { NotFound } from "@/routes/NotFound";

export function App() {
  return (
    <Routes>
      <Route element={<AppShell />}>
        <Route index element={<Dashboard />} />
        <Route path="ordenes" element={<Ordenes />} />
        <Route path="ordenes/nueva" element={<NuevaOrden />} />
        <Route path="ordenes/:numero" element={<OrdenDetalle />} />
        <Route path="*" element={<NotFound />} />
      </Route>
    </Routes>
  );
}
