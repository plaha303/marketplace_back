
import { ComponentType, SVGProps } from "react";
import FacebookIcon from "@/assets/Icons/FacebookIcon.svg?react";
import InstagramIcon from "@/assets/Icons/InstaIcon.svg?react";
import PinterestIcon from "@/assets/Icons/PinterestIcon.svg?react";

export type SocialLinksProps = {
  className?: string;
  colorIcon?: string;
}

export type SocialLinksType = {
  id: number;
  label?: string;
  path: string;
  icon: ComponentType<SVGProps<SVGSVGElement>>;
}

export const socialLinks: SocialLinksType[] = [
  {id: 1, icon: FacebookIcon, path: '/' },
  {id: 2, icon: InstagramIcon, path: '/'},
  {id: 3, icon: PinterestIcon, path: '/'},
] 
