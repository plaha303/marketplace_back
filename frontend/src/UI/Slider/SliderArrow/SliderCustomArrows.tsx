import { Button } from '@/UI/Button/Button';
import { Swiper as SwiperType } from 'swiper';
import LeftArrowSliderIcon from '@/assets/Icons/LeftArrowSliderIcon.svg?react'
import RightArrowSliderIcon from '@/assets/Icons/RightArrowSliderIcon.svg?react'

interface SliderCustomArrowsProps {
  swiperRef: React.RefObject<SwiperType | null>;
  isBeginning: boolean;
  isEnd: boolean;
}

function SliderCustomArrows({swiperRef, isBeginning, isEnd}: SliderCustomArrowsProps) {
  return (
    <div className="slider-controls flex gap-4 md:mt-8 mt-6">
      <div className='slider-button-prev'>
        <Button className='slider-btn-prev md:w-14 md:h-14 w-11 h-11 p-0' disabled={isBeginning} onClick={() => swiperRef.current?.slidePrev()}>
          <LeftArrowSliderIcon />
        </Button>
      </div>
      <div className='slider-button-next'>
        <Button className='slider-btn-next md:w-14 md:h-14 w-11 h-11 p-0' disabled={isEnd} onClick={() => swiperRef.current?.slideNext()}>
          <RightArrowSliderIcon />
        </Button>
      </div>
    </div>
  );
}

export default SliderCustomArrows;