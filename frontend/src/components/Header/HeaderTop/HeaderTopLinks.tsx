import AppRoute from "@/routers/enums/routers-enums";
import { ReactNode } from "react";
import FacebookIcon from "@/UI/Icons/FacebookIcon"
import InstaIcon from "@/UI/Icons/InstaIcon";
import PinterestIcon from "@/UI/Icons/PinterestIcon";

export type headerTopLinksProps = {
  id: number;
  label?: string;
  path: string;
  icon?: ReactNode;
}

export const headerTopLinks:headerTopLinksProps[] = [
  { id: 1, label: 'Про платформу', path: AppRoute.ABOUT },
  { id: 2, label: 'Контакти', path: AppRoute.CONTACT },
  { id: 3, label: 'Допомога', path: AppRoute.SUPPORT },
  { id: 4, label: 'Реєстрація', path: AppRoute.REGISTRATION },
]

export const headerTopLinksMobile: headerTopLinksProps[] = [
  {id: 1, icon: <FacebookIcon />, path: '/' },
  {id: 2, icon: <InstaIcon />, path: '/'},
  {id: 3, icon: <PinterestIcon />, path: '/'},
] 
