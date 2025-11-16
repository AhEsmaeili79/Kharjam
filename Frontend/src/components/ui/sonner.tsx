"use client";

import { Toaster as Sonner } from "sonner";
import { cn } from "@/lib/utils";

type ToasterProps = React.ComponentProps<typeof Sonner>;

export function Toaster({ className, ...props }: ToasterProps) {
  return (
    <Sonner
      className={cn("toaster group", className)}
      toastOptions={{
        classNames: {
          toast:
            "group toast bg-background text-foreground border shadow-lg rounded-xl px-5 py-3 flex items-center justify-center gap-3 text-sm font-medium",
          description: "text-muted-foreground text-xs",
          actionButton:
            "inline-flex h-8 items-center justify-center rounded-md bg-primary text-primary-foreground text-xs font-medium px-3 shadow transition-all hover:bg-primary/90",
          cancelButton:
            "inline-flex h-8 items-center justify-center rounded-md border text-xs font-medium px-3 shadow-sm hover:bg-accent",
        },
      }}
      {...props}
    />
  );
}
