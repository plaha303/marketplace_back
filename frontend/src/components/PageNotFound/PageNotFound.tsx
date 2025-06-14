import AppRoute from '@/routers/enums/routers-enums';
import { Button } from '@/UI/Button/Button';
import { Link } from 'react-router';

import style from "./PageNotFound.module.scss"

function PageNotFound() {
  return (
    <div className={`${style.page} pattern-bg lg:py-[64px] pb-0 pt-[64px] relative`}>
      <div className="container mx-auto px-4">
        <div className={style.page__inner}>
          <svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlnsXlink="http://www.w3.org/1999/xlink" style={{display:"none"}}>
            <defs>
              <filter id="stroke-text-svg-filter">
                <feMorphology operator="dilate" radius="3"></feMorphology>
                <feComposite operator="xor" in="SourceGraphic"/>
              </filter>
            </defs>
          </svg>

          <div className={`${style.page__title} text-center lg:mb-12 mb-8`}>НЕ ЗНАЙДЕНО</div>
          
          <div className="page__content lg:max-w-[565px] rounded-[32px] shadow-custom2 bg-snow-70">
            <div className="page__content-inner lg:p-12 p-6">
              <div className="page__content-title text-size-h3 leading-130 text-accent-800 font-bold uppercase lg:mb-10 mb-8">Ви заблукали?</div>
              <div className="page__content-text font-secondary text-size-body-1 leading-130 lg:mb-[56px] mb-8">
                Схоже, що сторінка, яку ви шукаєте, зникла безслідно. Але не хвилюйтеся, ми допоможемо вам знайти шлях!
              </div>
              <div className="page__content-buttons">
                <Button asChild className='btn-secondary text-size-body-2 font-bold py-4.5 px-10'>
                  <Link to={AppRoute.ROOT}>Головна</Link>
                </Button>
              </div>
            </div>
          </div>

          <div className={`${style.page__title_second} lg:mt-12 mt-8`}>СТОРІНКА 404</div>
        </div>
      </div>
    </div>
  );
}

export default PageNotFound;