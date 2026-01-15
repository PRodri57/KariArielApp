import { Link } from "react-router-dom";
import { Button } from "@/components/ui/Button";
import { useTheme } from "@/hooks/useTheme";
import lightModeIcon from "../../../Icons/light-mode.svg";
import nightModeIcon from "../../../Icons/night-mode.svg";

export function TopBar() {
  const { theme, toggleTheme } = useTheme();
  const isLight = theme === "light";
  const themeLabel = isLight ? "Modo oscuro" : "Modo claro";
  const iconSrc = isLight ? nightModeIcon : lightModeIcon;

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
        <Button
          size="sm"
          variant="outline"
          className="w-full sm:w-auto"
          onClick={toggleTheme}
          aria-pressed={isLight}
          aria-label={themeLabel}
          title={themeLabel}
        >
          <img src={iconSrc} alt="" className="h-5 w-5" />
        </Button>
      </div>
    </div>
  );
}
