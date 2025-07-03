import Heart from '@/assets/Icons/Heart.svg?react';
import User from '@/assets/Icons/User.svg?react';
import Tote from '@/assets/Icons/Tote.svg?react';
import Package from '@/assets/Icons/Package.svg?react';
import ChatDots from '@/assets/Icons/ChatDots.svg?react';
import Star from '@/assets/Icons/Star.svg?react';
import GearSix from '@/assets/Icons/GearSix.svg?react';
import Info from '@/assets/Icons/Info.svg?react';
import { ComponentType, SVGProps } from 'react';
import AppRoute from '@/routers/enums/routers-enums';

interface UserMenuLink {
  id: number;
  icon: ComponentType<SVGProps<SVGSVGElement>>;
  title: string;
  path: string;
}

export const userMenuLinks:UserMenuLink[] = [
  {id: 1, icon: Heart, title: 'Стати майстром', path: AppRoute.MASTER},
  {id: 2, icon: User, title: 'Мій профіль', path: AppRoute.PROFILE},
  {id: 3, icon: Tote, title: 'Мої замовлення', path: AppRoute.ORDERS},
  {id: 4, icon: Package, title: 'Мої товари', path: AppRoute.GOODS},
  {id: 5, icon: Heart, title: 'Обране', path: AppRoute.FAVORITE},
  {id: 6, icon: ChatDots, title: 'Повідомлення', path: AppRoute.NOTIFICATION},
  {id: 7, icon: Star, title: 'Відгуки', path: AppRoute.REVIEWS}
]

export const userMenuLinksSettings:UserMenuLink[] = [
  {id: 1, icon: GearSix, title: 'Налаштування', path: AppRoute.SETTINGS},
  {id: 2, icon: Info, title: 'Допомога', path: AppRoute.SUPPORT},
]