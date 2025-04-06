import Slider, {Settings} from "react-slick";
import {SliderButton, SliderProps} from "./interface"
import SliderItem from './SLiderItem';
import SliderPrevIcon from "./Icons/SliderPrevIcon"
import SliderNextIcon from "./Icons/SliderNextIcon"

import styles from "./Slider.module.scss"
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import { useRef } from "react";

function CustomArrowPrev(props: SliderButton) {
  const {onClick } = props;
  return (
    <button type="button" className={`${styles.arrowBtn} ${styles.arrowBtn__left}`} onClick={onClick}>
      <SliderPrevIcon color="#041C4F" />
    </button>
  )
}

function CustomArrowNext(props: SliderButton) {
  const {onClick } = props;
  return (
    <button type="button" className={`${styles.arrowBtn}  ${styles.arrowBtn__right}`} onClick={onClick}>
      <SliderNextIcon color="#041C4F" />
    </button>
  )
}

function ImageSlider({
	dots = false,
	speed = 500,
	slidesToShow = 1,
	slidesToScroll = 1,
	arrows = true,
	centerMode = false,
	centerPadding = '0',
	sliders,
	infinite = false,
  titleClass,
  descriptionClass
}: SliderProps) {


	const settings: Settings = {
		dots,
		speed,
		slidesToShow,
		slidesToScroll,
		arrows,
		dotsClass: 'button-bar',
		centerMode,
		centerPadding: `${centerPadding}px`,
		infinite,
		prevArrow: <CustomArrowPrev />,
		nextArrow: <CustomArrowNext />,
	};

	return (
		<div className="slider-container">
			<Slider  {...settings}>
				{sliders.map((slide) => (
					<SliderItem key={slide.id} slide={slide} titleClass={titleClass} descriptionClass={descriptionClass} />
				))}
			</Slider>
		</div>
	);
}

export default ImageSlider;