import { FC } from "react";
import { IconProps } from "./interface";

export const XIcon: FC<IconProps> = ({ className, ...props }) => {
  return (
    <svg
      fill="none"
      strokeWidth="2"
      viewBox="0 0 24 24"
      stroke="currentColor"
      strokeLinecap="round"
      strokeLinejoin="round"
      xmlns="http://www.w3.org/2000/svg"
      className={`lucide lucide-x-icon lucide-x ${className ?? ""}`}
      {...props}
    >
       <path d="M18 6 6 18" />
       <path d="m6 6 12 12" />
    </svg>
  );
};
