import FacebookIcon from "@/UI/Icons/FacebookIcon"
import InstaIcon from "@/UI/Icons/InstaIcon";
import PinterestIcon from "@/UI/Icons/PinterestIcon";
import { ReactNode } from "react";

export type SocialLinksProps = {
  id: number;
  label?: string;
  path: string;
  icon?: ReactNode;
}

export const socialLinks: SocialLinksProps[] = [
  {id: 1, icon: <FacebookIcon />, path: '/' },
  {id: 2, icon: <InstaIcon />, path: '/'},
  {id: 3, icon: <PinterestIcon />, path: '/'},
] 
