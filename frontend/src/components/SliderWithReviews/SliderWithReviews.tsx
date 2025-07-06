import BaseSlider from "@/UI/Slider/BaseSlider";
import { PlatformReviewsItem } from "@/utils/packages/platformReviews/type/interface";
import { Link } from "react-router";
import ReviewBlock from "../ReviewBlock/ReviewBlock";

interface SliderWithReviewsProps {
  title: string;
  watchAll: string,
  data: PlatformReviewsItem[]
}

function SliderWithReviews({title, watchAll, data}: SliderWithReviewsProps) {
  return (
    <div className="slider-review lg:py-[80px] py-12">
      <div className="container px-4 mx-auto">
        <div className="slider-review__header lg:mb-16 mb-9 flex md:items-center justify-between md:flex-row flex-col md:gap-0 gap-4">
          <h3 className="m:text-size-h3 text-size-h2 uppercase text-accent-800 font-bold leading-130">{title}</h3>
          <Link to={watchAll} className="font-secondary underline text-size-body-3 leading-100 text-primary-600">дивитися всі</Link>
        </div>
        <div className="slider-review__body overflow-hidden sm:mr-0 -mr-4">
          <BaseSlider
            spaceBetween={36}
            navigation={true}
            slidesPerView={3}
            className="sliderWithBlocks"
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
                slidesPerView: 3,
                spaceBetween: 36,
              },
            }}
          >
            {data.map(review => (
              <ReviewBlock review={review} />
            ))}
          </BaseSlider>
        </div>
      </div>
    </div>
  );
}

export default SliderWithReviews;