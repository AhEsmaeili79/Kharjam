import { FC } from "react";
import { IconProps } from "./interface";

export const UserNameIcon: FC<IconProps> = ({ className, ...props }) => {
  return (
    <svg
      fill="none"
      viewBox="0 0 24 24"
      stroke="currentColor"
      strokeLinecap="round"
      strokeLinejoin="round"
      xmlns="http://www.w3.org/2000/svg"
      className={`lucide lucide-contact-round-icon lucide-contact-round ${
        className ?? ""
      }`}
      {...props}
    >
      <path d="M16 2v2" />
      <path d="M17.915 22a6 6 0 0 0-12 0" />
      <path d="M8 2v2" />
      <circle cx="12" cy="12" r="4" />
      <rect x="3" y="4" width="18" height="18" rx="2" />
    </svg>
  );
};
