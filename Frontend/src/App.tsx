import { Route, Routes } from "react-router-dom";
import { AppShell } from "@/components/layout/AppShell";
import { ClienteDetalle } from "@/routes/ClienteDetalle";
import { Clientes } from "@/routes/Clientes";
import { Dashboard } from "@/routes/Dashboard";
import { NuevoCliente } from "@/routes/NuevoCliente";
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
        <Route path="clientes" element={<Clientes />} />
        <Route path="clientes/nuevo" element={<NuevoCliente />} />
        <Route path="clientes/:id" element={<ClienteDetalle />} />
        <Route path="*" element={<NotFound />} />
      </Route>
    </Routes>
  );
}
