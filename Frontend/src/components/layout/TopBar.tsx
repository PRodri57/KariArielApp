import { Link } from "react-router-dom";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";

export function TopBar() {
  return (
    <div className="glass flex flex-col gap-4 rounded-3xl p-5 shadow-soft md:flex-row md:items-center md:justify-between">
      <div>
        <p className="text-xs uppercase tracking-[0.25em] text-ink/50">Panel</p>
        <h2 className="mt-2 text-2xl">Ordenes</h2>
      </div>

      <div className="flex w-full flex-col gap-3 md:w-auto md:flex-row md:items-center">
        <Input placeholder="Buscar orden #" aria-label="Buscar orden" />
        <Link to="/ordenes/nueva">
          <Button size="md">Nueva orden</Button>
        </Link>
      </div>
    </div>
  );
}
