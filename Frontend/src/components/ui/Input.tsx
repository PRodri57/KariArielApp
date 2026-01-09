import * as React from "react";
import { cn } from "@/lib/utils";

export type InputProps = React.InputHTMLAttributes<HTMLInputElement>;

export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, ...props }, ref) => (
    <input
      ref={ref}
      className={cn(
        "h-11 w-full rounded-2xl border border-ink/15 bg-haze/80 px-4 text-sm text-ink shadow-sm transition placeholder:text-ink/40 focus:border-ember/70 focus:outline-none focus:ring-2 focus:ring-ember/30",
        className
      )}
      {...props}
    />
  )
);

Input.displayName = "Input";
