import BaseSlider from "@/UI/Slider/BaseSlider";
import ProductCardAuction from "../ProductCard/ProductCardAuction";
import { productsAuction } from "./type/interface";
import { EffectCards } from 'swiper/modules';
import 'swiper/css/effect-cards';
import { useMediaQuery } from "react-responsive";

function SliderAuction() {
  const isMore1280 = useMediaQuery({query: '(min-width: 1280px)'})

  return (
    <div className="auction-slider overflow-hidden sm:mr-0 sm:ml-0 -ml-4 -mr-4">
      <BaseSlider 
        navigation={true} 
        effect={isMore1280 ? "cards" : undefined}
        grabCursor={isMore1280}
        modules={isMore1280 ? [EffectCards] : []}
        className="home-auction-slider"
        onRealIndexChange={(swiper) => {
          if (isMore1280) {
            swiper.allowTouchMove = false;
            swiper.unsetGrabCursor();
          }
        }}
        onTouchEnd={(swiper) => {
          if (isMore1280) {
            swiper.allowTouchMove = true;
          }
        }}
        {...(isMore1280 && {
          cardsEffect: {
            perSlideOffset: 18,
            perSlideRotate: 0,
            rotate: false,
            slideShadows: false,
          }
        })}

        breakpoints={{
          0: {
            slidesPerView: "auto",
            spaceBetween: 16,
          },
          640: {
            slidesPerView: 1.5,
            spaceBetween: 16,
          },
          768: {
            slidesPerView: 2,
            spaceBetween: 20,
          },
          1024: {
            slidesPerView: 2.5,
            spaceBetween: 26,
          },
          1280: {
            slidesPerView: 1,
            spaceBetween: 0,
          },
        }}
      >
        {productsAuction.map(product => (
          <ProductCardAuction key={product.id} product={product} />
        ))}
      </BaseSlider>
    </div>
  );
}

export default SliderAuction;