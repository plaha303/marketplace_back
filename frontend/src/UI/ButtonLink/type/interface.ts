import { ReactNode } from "react";
import { LinkProps } from "react-router";

export interface ButtonLinkProps extends LinkProps {
  children: ReactNode,
  className?: string
}