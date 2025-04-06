export interface SliderProps {
  dots?: boolean,
  speed?: number,
  slidesToShow?: number,
  slidesToScroll?: number,
  arrows?: boolean,
  centerMode?: boolean,
  centerPadding?: string,
  infinite?: boolean,
  sliders: Slide[],
  titleClass?: string,
  descriptionClass?: string
}

export interface Slide { 
  title: string,
  description: string,
  id: number,
  imgSrc: string,
  textBtn: string,
  link: string
}

export interface SliderItemProps {
  slide: Slide,
  titleClass?: string,
  descriptionClass?: string
}

export interface SliderButton {
  onClick?: () => void,
  className?: string,
  style?: string,
}

export interface SliderIconProps {
  color: string,
  size?: string,
  className?: string
}