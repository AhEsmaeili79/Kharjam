import { FC } from "react";
import { IconProps } from "./interface";

export const DollarIcon: FC<IconProps> = ({ className, ...props }) => {
  return (
    <svg
      fill="none"
      strokeWidth="2"
      viewBox="0 0 24 24"
      stroke="currentColor"
      strokeLinecap="round"
      strokeLinejoin="round"
      xmlns="http://www.w3.org/2000/svg"
      className={`lucide lucide-dollar-sign-icon lucide-dollar-sign ${className ?? ""}`}
      {...props}
    >
         <line x1="12" x2="12" y1="2" y2="22"/>
         <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
    </svg>
  );
};
