import { FC } from "react";
import { IconProps } from "./interface";

export const CheckICon: FC<IconProps> = ({ className, ...props }) => {
  return (
    <svg
      fill="none"
      viewBox="0 0 24 24"
      stroke="currentColor"
      strokeLinecap="round"
      strokeLinejoin="round"
      xmlns="http://www.w3.org/2000/svg"
      className={`lucide lucide-check-icon lucide-check ${className ?? ""}`}
      {...props}
    >
      <path d="M20 6 9 17l-5-5" />
    </svg>
  );
};
