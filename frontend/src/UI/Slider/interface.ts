export interface SliderProps {
  dots?: boolean,
  speed?: number,
  slidesToShow?: number,
  slidesToScroll?: number,
  arrows?: boolean,
  centerMode?: boolean,
  centerPadding?: string,
  infinite?: boolean,
  sliders: Slide[]
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
  slide: Slide;
}