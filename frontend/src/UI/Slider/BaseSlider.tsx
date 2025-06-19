import React from 'react';
import { BaseSliderProps } from './type/interface';
import { Swiper, SwiperSlide } from 'swiper/react';
import { Navigation, Pagination } from 'swiper/modules';

import 'swiper/css';
import 'swiper/css/navigation';
import 'swiper/css/pagination';

import './generalSliderStyle.scss'

function BaseSlider({children, className, ...props}: BaseSliderProps) {
  return (
    <div className='relative'>
      <Swiper
        modules={[Navigation, Pagination]}
        navigation={props.navigation ? true : false}
        pagination={props.pagination ? { clickable: true } : false}
        className={className}
        {...props}
      >
        {React.Children.map(children, (child, index) => (
          <SwiperSlide key={index}>{child}</SwiperSlide>
        ))}
      </Swiper>
    </div>
  );
}

export default BaseSlider;