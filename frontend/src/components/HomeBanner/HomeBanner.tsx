import AppRoute from "@/routers/enums/routers-enums";
import { Button } from "@/UI/Button/Button";
import BaseSlider from "@/UI/Slider/BaseSlider";
import { Link } from "react-router";
import HomeBannerImg from '@/assets/homeBanner/homeBannerImg.svg?react'

import style from "./HomeBanner.module.scss"

function HomeBanner() {
  return (
    <div className="home-banner pattern-bg lg:pt-6 lg:pb-12 py-12">
      <div className="container px-4 mx-auto">
        <BaseSlider pagination={true}>
          <div className="home-banner__slide slide">
            <div className="slide__inner flex items-center justify-between lg:gap-6">
              <div className="slide__left">
                <div className="slide__content lg:p-12 md:p-6 p-4 bg-snow rounded-4xl shadow-custom2 max-w-[566px]">
                  <div className="slide__content-body">
                    <div className="slide__content-title leading-130 uppercase text-size-h1 text-accent-800 lg:mb-10 md:mb-8 mb-4">
                      Відкрий світ унікальних виробів
                    </div>
                    <div className="slide__content-text">
                      <p className="font-secondary text-size-body-1 leading-130">Обирай те, що справді важливе! Купуй або продавай хендмейд вироби. </p>
                      <p className="font-secondary text-size-body-1 leading-130">Підтримуй майстрів, створюй унікальні подарунки та знаходь те, що цінне для тебе і твоїх близьких.</p>
                    </div>
                  </div>
                  <div className="slide__content-btns flex md:gap-4 gap-2 lg:mt-14 mt-8">
                    <Button asChild className="btn-primary text-size-body-2 font-bold leading-100 md:py-[18px] md:px-10 p-4">
                      <Link to={AppRoute.REGISTRATION}>Реєстрація</Link>
                    </Button>
                    <Button asChild className="btn-secondary text-size-body-2 font-bold leading-100 md:py-[18px] md:px-10 p-4">
                      <Link to={AppRoute.ROOT}>Аукціон</Link>
                    </Button>
                  </div>
                </div>
              </div>
              <div className="slide__right relative pl-6 w-[58%]">
                <div className={`${style.infoBlock} ${style.one} bg-primary-900 rounded-4xl py-6 px-8 flex items-center justify-center w-[200px] h-[200px] flex-col`}>
                  <div className="info-block__title text-size-h2 text-snow text-center leading-100 mb-3">5k+</div>
                  <div className="info-block__text text-size-h6 leading-130 text-snow text-center">Товарів</div>
                </div>
                <div className={`${style.infoBlock} ${style.two} bg-primary-900 rounded-4xl py-6 px-8 flex items-center justify-center w-[200px] h-[200px] flex-col`}>
                  <div className="info-block__title text-size-h2 text-snow text-center leading-100 mb-3">500</div>
                  <div className="info-block__text text-size-h6 leading-130 text-snow text-center">Аукціонів</div>
                </div>
                <div className={`${style.infoBlock} ${style.three} bg-primary-900 rounded-4xl py-6 px-8 flex items-center justify-center w-[200px] h-[200px] flex-col`}>
                  <div className="info-block__title text-size-h2 text-snow text-center leading-100 mb-3">5k+</div>
                  <div className="info-block__text text-size-h6 leading-130 text-snow text-center">Майстрів</div>
                </div>
                <HomeBannerImg />
              </div>
            </div>
          </div>
        </BaseSlider>
      </div>
    </div>
  );
}

export default HomeBanner;