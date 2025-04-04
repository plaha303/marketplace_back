import Slider, {Settings} from "react-slick";
import {SliderProps} from "./interface"
import SliderItem from './SLiderItem';

import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";



function ImageSlider({dots = false, speed = 500, slidesToShow = 1, slidesToScroll = 1, arrows, centerMode = false, centerPadding = "0", sliders, infinite = false}: SliderProps) {
  const settings: Settings = {
    dots,
    speed,
    slidesToShow,
    slidesToScroll,
    arrows,
    dotsClass: 'button-bar',
    centerMode,
    centerPadding: `${centerPadding}px`,
    infinite
  }

  return (
    <div className="slider-container">
      <Slider {...settings}>
        {sliders.map(slide => (
          <div>
            <SliderItem key={slide.id} slide={slide} />
          </div>
        ))}
      </Slider>
    </div>
  );
}

export default ImageSlider;