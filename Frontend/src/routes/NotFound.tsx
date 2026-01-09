import { Link } from "react-router-dom";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";

export function NotFound() {
  return (
    <Card className="text-center">
      <p className="text-sm uppercase tracking-[0.3em] text-ink/40">404</p>
      <h2 className="mt-2 text-3xl">Esta ruta no existe</h2>
      <Link to="/" className="mt-4 inline-flex">
        <Button variant="secondary">Ir al inicio</Button>
      </Link>
    </Card>
  );
}
