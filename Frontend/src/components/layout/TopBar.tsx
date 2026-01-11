import { Link } from "react-router-dom";
import { Button } from "@/components/ui/Button";

export function TopBar() {
  return (
    <div className="glass flex flex-col gap-4 rounded-3xl p-5 shadow-soft md:flex-row md:items-center md:justify-between">
      <div>
        <p className="text-xs uppercase tracking-[0.25em] text-ink/50">Panel</p>
        <h2 className="mt-2 text-2xl">Gestion diaria</h2>
      </div>

      <div className="flex w-full flex-col gap-3 md:w-auto md:flex-row md:items-center">
        <div className="flex flex-col gap-2 sm:flex-row">
          <Link to="/ordenes/nueva">
            <Button size="md">Nueva orden</Button>
          </Link>
          <Link to="/clientes/nuevo">
            <Button size="md" variant="secondary">
              Nuevo cliente
            </Button>
          </Link>
        </div>
      </div>
    </div>
  );
}
