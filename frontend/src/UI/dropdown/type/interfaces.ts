import { ReactNode } from "react";

export interface DropDownProps {
  children: ReactNode | ((closeMenu: () => void) => ReactNode),
  buttonContent: ReactNode,
  classNameButton?: string,
  classNameMenu?: string
}