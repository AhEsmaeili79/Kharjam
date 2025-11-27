import { FC } from "react";
import { IconProps } from "./interface";

export const CreditCardIcon: FC<IconProps> = ({ className, ...props }) => {
  return (
    <svg
      fill="none"
      strokeWidth="2"
      viewBox="0 0 24 24"
      stroke="currentColor"
      strokeLinecap="round"
      strokeLinejoin="round"
      xmlns="http://www.w3.org/2000/svg"
      className={`lucide lucide-credit-card-icon lucide-credit-card ${
        className ?? ""
      }`}
    >
      <rect width="20" height="14" x="2" y="5" rx="2" />
      <line x1="2" x2="22" y1="10" y2="10" />
    </svg>
  );
};
