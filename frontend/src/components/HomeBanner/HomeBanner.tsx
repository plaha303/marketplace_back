import AppRoute from "@/routers/enums/routers-enums";
import { Button } from "@/UI/Button/Button";
import BaseSlider from "@/UI/Slider/BaseSlider";
import { Link } from "react-router";
import HomeBannerImg from '@/assets/homeBanner/homeBannerImg.svg?react'

import style from "./HomeBanner.module.scss"

function HomeBanner() {
  return (
    <div className="home-banner pattern-bg lg:py-6 py-12">
      <div className="container px-4 mx-auto">
        <BaseSlider 
          pagination={true} 
          spaceBetween={10}
          className="home-banner"
        >
          <div className="home-banner__slide slide">
            <div className="slide__inner flex items-center justify-between lg:gap-6 gap-9 lg:flex-row flex-col">
              <div className="slide__left lg:order-1 order-2">
                <div className="slide__content lg:p-12 md:p-6 p-4 bg-snow rounded-4xl shadow-custom2 max-w-[566px]">
                  <div className="slide__content-body">
                    <div className="slide__content-title leading-130 uppercase xl:text-size-h1 lg:text-size-h5 md:text-size-h3 text-size-h1 text-accent-800 lg:mb-10 md:mb-8 mb-4">
                      Відкрий світ унікальних виробів
                    </div>
                    <div className="slide__content-text">
                      <p className="font-secondary xl:text-size-body-1 lg:text-size-body-3 md:text-size-body-2 text-size-body-3 leading-130">Обирай те, що справді важливе! Купуй або продавай хендмейд вироби. </p>
                      <p className="font-secondary xl:text-size-body-1 lg:text-size-body-3 md:text-size-body-2 text-size-body-3 leading-130">Підтримуй майстрів, створюй унікальні подарунки та знаходь те, що цінне для тебе і твоїх близьких.</p>
                    </div>
                  </div>
                  <div className="slide__content-btns flex md:gap-4 gap-2 lg:mt-14 mt-8">
                    <Button asChild variant="default" className="md:text-size-body-2 text-size-body-3 font-bold leading-100 md:py-[18px] md:px-10 p-4">
                      <Link to={AppRoute.REGISTRATION}>Реєстрація</Link>
                    </Button>
                    <Button asChild variant="secondary" className="md:text-size-body-2 text-size-body-3 font-bold leading-100 md:py-[18px] md:px-10 p-4">
                      <Link to={AppRoute.ROOT}>Аукціон</Link>
                    </Button>
                  </div>
                </div>
              </div>
              <div className="slide__right relative lg:pl-6 lg:w-[58%] lg:order-2 order-1">
                <div className={`${style.infoBlock} ${style.one} bg-primary-900 xl:rounded-4xl lg:rounded-2xl xl:py-6 xl:px-8 lg:py-3 lg:px-4 p-2 flex items-center justify-center xl:w-[200px] xl:h-[200px] lg:w-[98px] lg:h-[98px] md:w-[150px] md:h-[150px] w-[96px] h-[96px] md:rounded-4xl rounded-2xl flex-col`}>
                  <div className="info-block__title xl:text-size-h2 lg:text-size-h5 text-size-h2 text-snow text-center leading-100 md:mb-3 mb-1">5k+</div>
                  <div className="info-block__text xl:text-size-h6 lg:text-size-h7 md:text-size-h6 leading-130 text-snow text-center">Товарів</div>
                </div>
                <div className={`${style.infoBlock} ${style.two} bg-primary-900 xl:rounded-4xl lg:rounded-2xl xl:py-6 xl:px-8 lg:py-3 lg:px-4 flex items-center justify-center xl:w-[200px] xl:h-[200px] lg:w-[98px] lg:h-[98px] md:w-[150px] md:h-[150px] w-[96px] h-[96px] md:rounded-4xl rounded-2xl flex-col`}>
                  <div className="info-block__title xl:text-size-h2 lg:text-size-h5 text-size-h2 text-snow text-center leading-100 md:mb-3 mb-1">500</div>
                  <div className="info-block__text xl:text-size-h6 lg:text-size-h7 md:text-size-h6 leading-130 text-snow text-center">Аукціонів</div>
                </div>
                <div className={`${style.infoBlock} ${style.three} bg-primary-900 xl:rounded-4xl lg:rounded-2xl xl:py-6 xl:px-8 lg:py-3 lg:px-4 flex items-center justify-center xl:w-[200px] xl:h-[200px] lg:w-[98px] lg:h-[98px] md:w-[150px] md:h-[150px] w-[96px] h-[96px] md:rounded-4xl rounded-2xl flex-col`}>
                  <div className="info-block__title xl:text-size-h2 lg:text-size-h5 text-size-h2 text-snow text-center leading-100 md:mb-3 mb-1">5k+</div>
                  <div className="info-block__text xl:text-size-h6 lg:text-size-h7 md:text-size-h6 leading-130 text-snow text-center">Майстрів</div>
                </div>
                <HomeBannerImg className="xl:w-auto lg:w-full xl:h-auto lg:h-full w-full h-full" />
              </div>
            </div>
          </div>

          <div className="home-banner__slide slide">
            <div className="slide__inner flex items-center justify-between lg:gap-6 gap-9 lg:flex-row flex-col">
              <div className="slide__left lg:order-1 order-2">
                <div className="slide__content lg:p-12 md:p-6 p-4 bg-snow rounded-4xl shadow-custom2 max-w-[566px]">
                  <div className="slide__content-body">
                    <div className="slide__content-title leading-130 uppercase xl:text-size-h1 lg:text-size-h5 md:text-size-h3 text-size-h1 text-accent-800 lg:mb-10 md:mb-8 mb-4">
                      Другий слайд
                    </div>
                    <div className="slide__content-text">
                      <p className="font-secondary xl:text-size-body-1 lg:text-size-body-3 md:text-size-body-2 text-size-body-3 leading-130">It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. </p>
                      <p className="font-secondary xl:text-size-body-1 lg:text-size-body-3 md:text-size-body-2 text-size-body-3 leading-130">It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. </p>
                    </div>
                  </div>
                  <div className="slide__content-btns flex md:gap-4 gap-2 lg:mt-14 mt-8">
                    <Button asChild className="btn-primary md:text-size-body-2 text-size-body-3 font-bold leading-100 md:py-[18px] md:px-10 p-4">
                      <Link to={AppRoute.REGISTRATION}>Реєстрація</Link>
                    </Button>
                    <Button asChild className="btn-secondary md:text-size-body-2 text-size-body-3 font-bold leading-100 md:py-[18px] md:px-10 p-4">
                      <Link to={AppRoute.ROOT}>Аукціон</Link>
                    </Button>
                  </div>
                </div>
              </div>
              <div className="slide__right relative lg:pl-6 lg:w-[58%] lg:order-2 order-1">
                <div className={`${style.infoBlock} ${style.one} bg-primary-900 xl:rounded-4xl lg:rounded-2xl xl:py-6 xl:px-8 lg:py-3 lg:px-4 p-2 flex items-center justify-center xl:w-[200px] xl:h-[200px] lg:w-[98px] lg:h-[98px] md:w-[150px] md:h-[150px] w-[96px] h-[96px] md:rounded-4xl rounded-2xl flex-col`}>
                  <div className="info-block__title xl:text-size-h2 lg:text-size-h5 text-size-h2 text-snow text-center leading-100 md:mb-3 mb-1">5k+</div>
                  <div className="info-block__text xl:text-size-h6 lg:text-size-h7 md:text-size-h6 leading-130 text-snow text-center">Товарів</div>
                </div>
                <div className={`${style.infoBlock} ${style.two} bg-primary-900 xl:rounded-4xl lg:rounded-2xl xl:py-6 xl:px-8 lg:py-3 lg:px-4 flex items-center justify-center xl:w-[200px] xl:h-[200px] lg:w-[98px] lg:h-[98px] md:w-[150px] md:h-[150px] w-[96px] h-[96px] md:rounded-4xl rounded-2xl flex-col`}>
                  <div className="info-block__title xl:text-size-h2 lg:text-size-h5 text-size-h2 text-snow text-center leading-100 md:mb-3 mb-1">500</div>
                  <div className="info-block__text xl:text-size-h6 lg:text-size-h7 md:text-size-h6 leading-130 text-snow text-center">Аукціонів</div>
                </div>
                <div className={`${style.infoBlock} ${style.three} bg-primary-900 xl:rounded-4xl lg:rounded-2xl xl:py-6 xl:px-8 lg:py-3 lg:px-4 flex items-center justify-center xl:w-[200px] xl:h-[200px] lg:w-[98px] lg:h-[98px] md:w-[150px] md:h-[150px] w-[96px] h-[96px] md:rounded-4xl rounded-2xl flex-col`}>
                  <div className="info-block__title xl:text-size-h2 lg:text-size-h5 text-size-h2 text-snow text-center leading-100 md:mb-3 mb-1">5k+</div>
                  <div className="info-block__text xl:text-size-h6 lg:text-size-h7 md:text-size-h6 leading-130 text-snow text-center">Майстрів</div>
                </div>
                <HomeBannerImg className="xl:w-auto lg:w-full xl:h-auto lg:h-full w-full h-full" />
              </div>
            </div>
          </div>
        </BaseSlider>
      </div>
    </div>
  );
}

export default HomeBanner;