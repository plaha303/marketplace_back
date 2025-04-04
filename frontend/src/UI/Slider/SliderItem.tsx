import { Link } from "react-router";
import {SliderItemProps} from "./interface"
import styles from "./SliderItem.module.scss"


function SliderItem({slide}: SliderItemProps) {

  return (
    <div className={`${styles.slideBlock} block`}>
      <div className={`${styles.slideBlock__inner} flex items-center`}>
        <div className={`${styles.slideBlock__left} flex-1 pr-5`}>
          <div className={`${styles.slideBlock__title}`}>{slide.title}</div>
          <div>{slide.description}</div>
          <Link to={slide.link} className="d-block rounded-lg text-white font-semibold text-2xl custom-boxShadow py-4 px-[36px] leading-[36px] btn-blue">
            {slide.textBtn}
          </Link>
        </div>
        <div className={`${styles.slideBlock__right} max-w-[640px]`}>
          <img src={slide.imgSrc} alt={slide.title} className="rounded-3xl w-full" />
        </div>
      </div>
    </div>
  );
}

export default SliderItem;