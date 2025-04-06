import {SliderItemProps} from "./interface"
import styles from "./SliderItem.module.scss"
import Button from "../Button/Button"


function SliderItem({slide, descriptionClass, titleClass}: SliderItemProps) {

  return (
    <div className={`${styles.slideBlock__inner || ''} flex items-center`}>
      <div className={`${styles.slideBlock__left || ''} flex-1 pr-5`}>
        <div className={`${titleClass} lg:mb-[32px]`}>{slide.title}</div>
        <div className={`${descriptionClass} font-medium text-xl`}>{slide.description}</div>
        <div className="mt-6">
          <Button type="button" className="inline-block text-2xl py-4 px-[36px] leading-[36px] btn-blue">
            {slide.textBtn}
          </Button>
        </div>
      </div>
      <div className={`${styles.slideBlock__right || ''} max-w-[640px]`}>
        <img src={slide.imgSrc} alt={slide.title} className="rounded-3xl w-full" />
      </div>
    </div>
  );
}

export default SliderItem;