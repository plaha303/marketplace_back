import { ReactNode } from "react";
import { SwiperProps } from "swiper/react";

export interface BaseSliderProps extends SwiperProps { 
  children: ReactNode;
  className?: string;
}