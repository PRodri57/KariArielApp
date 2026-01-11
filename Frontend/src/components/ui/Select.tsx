import * as React from "react";
import { cn } from "@/lib/utils";

export type SelectProps = React.SelectHTMLAttributes<HTMLSelectElement>;

export const Select = React.forwardRef<HTMLSelectElement, SelectProps>(
  ({ className, ...props }, ref) => (
    <select
      ref={ref}
      className={cn(
        "h-11 w-full rounded-2xl border border-ink/15 bg-haze/80 px-4 text-sm text-ink shadow-sm transition placeholder:text-ink/40 focus:border-ember/70 focus:outline-none focus:ring-2 focus:ring-ember/30 disabled:cursor-not-allowed disabled:opacity-60",
        className
      )}
      {...props}
    />
  )
);

Select.displayName = "Select";
