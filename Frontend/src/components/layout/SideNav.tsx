import { NavLink } from "react-router-dom";
import { cn } from "@/lib/utils";

const navItems = [
  { to: "/", label: "Dashboard" },
  { to: "/ordenes", label: "Ordenes" },
  { to: "/clientes", label: "Clientes" }
];

export function SideNav() {
  return (
    <aside className="glass flex flex-col gap-6 rounded-3xl p-6 shadow-soft lg:sticky lg:top-6 lg:h-fit">
      <div>
        <p className="text-xs uppercase tracking-[0.3em] text-ink/50">Kari Ariel</p>
        <h1 className="mt-2 text-2xl">Panel</h1>
      </div>

      <nav className="flex flex-col gap-2">
        {navItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            className={({ isActive }) =>
              cn(
                "rounded-2xl px-4 py-3 text-sm font-semibold transition",
                isActive
                  ? "bg-soot text-white shadow-soft"
                  : "text-ink/70 hover:bg-ink/5"
              )
            }
          >
            {item.label}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}
