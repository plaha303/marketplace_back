import Category from "@/routers/enums/category";
import { ReactNode } from "react";

export type MenuLinksSectionProps = {
  handleOpenMenuCatalog: () => void;
  openMenuCatalog?: boolean;
  buttonRef?: React.RefObject<HTMLButtonElement | null>;
}
export type MenuProps = {
  handleOpenMenuCatalog: () => void;
  openMenuCatalog?: boolean;
}

export type CatalogLinksProps = {
  id: number,
  label: string,
  icon: ReactNode,
  categoryId: Category
}