import { Dispatch, SetStateAction } from "react";

export type HeaderBottomProps = {
  setActiveHamburger: Dispatch<SetStateAction<boolean>>;
  activeHamburger?: boolean;
  handleOpenUserMenu: () => void;
}