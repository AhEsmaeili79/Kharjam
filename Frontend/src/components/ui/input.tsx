import * as React from "react"

import { cn } from "@/lib/utils"

export interface InputProps
  extends React.InputHTMLAttributes<HTMLInputElement> {
  addonBefore?: React.ReactNode
  addonAfter?: React.ReactNode
}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, type = "text", addonBefore, addonAfter, ...props }, ref) => {
    const hasBefore = addonBefore !== undefined && addonBefore !== null
    const hasAfter = addonAfter !== undefined && addonAfter !== null

    return (
      <div className="relative w-full">
        {hasBefore ? (
          <div className="absolute inset-y-0 left-0 pl-4 flex items-center">
            {addonBefore}
          </div>
        ) : null}
        {hasAfter ? (
          <div className="absolute inset-y-0 right-0 pr-4 flex items-center">
            {addonAfter}
          </div>
        ) : null}
        <input
          ref={ref}
          type={type}
          className={cn(
            "flex h-14 w-full rounded-xl border outline-none bg-input border-sky-500 dark:border-none pl-4 pr-12 py-2 text-sm shadow-xs transition-colors placeholder:text-text-secondary text-text-base disabled:opacity-50 disabled:cursor-not-allowed hover:bg-sky-50 hover:dark:bg-input/70",
            hasBefore && "pl-12",
            hasAfter && "pr-12",
            className
          )}
          {...props}
        />
      </div>
    )
  }
)

Input.displayName = "Input"

export { Input }


