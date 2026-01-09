import { Outlet } from "react-router-dom";
import { SideNav } from "@/components/layout/SideNav";
import { TopBar } from "@/components/layout/TopBar";

export function AppShell() {
  return (
    <div className="relative min-h-screen overflow-hidden">
      <div className="pointer-events-none absolute -top-32 right-0 h-72 w-72 rounded-full bg-ember/20 blur-3xl" />
      <div className="pointer-events-none absolute bottom-0 left-0 h-96 w-96 rounded-full bg-sea/20 blur-3xl" />

      <div className="relative mx-auto flex min-h-screen max-w-6xl flex-col gap-6 px-4 py-6 lg:grid lg:grid-cols-[240px_1fr]">
        <SideNav />
        <div className="flex flex-1 flex-col gap-6">
          <TopBar />
          <Outlet />
        </div>
      </div>
    </div>
  );
}
