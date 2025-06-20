import { ReactNode } from "react";
import { SwiperProps } from "swiper/react";
import { PaginationOptions } from "swiper/types";

export interface BaseSliderProps extends SwiperProps { 
  children: ReactNode;
  className?: string;
  pagination?: boolean | PaginationOptions;
}