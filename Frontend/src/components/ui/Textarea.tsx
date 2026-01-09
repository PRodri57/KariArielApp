import * as React from "react";
import { cn } from "@/lib/utils";

export type TextareaProps = React.TextareaHTMLAttributes<HTMLTextAreaElement>;

export const Textarea = React.forwardRef<HTMLTextAreaElement, TextareaProps>(
  ({ className, ...props }, ref) => (
    <textarea
      ref={ref}
      className={cn(
        "min-h-[120px] w-full rounded-2xl border border-ink/15 bg-haze/80 px-4 py-3 text-sm text-ink shadow-sm transition placeholder:text-ink/40 focus:border-ember/70 focus:outline-none focus:ring-2 focus:ring-ember/30",
        className
      )}
      {...props}
    />
  )
);

Textarea.displayName = "Textarea";
