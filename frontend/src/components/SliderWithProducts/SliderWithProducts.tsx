import { Link } from "react-router";
import { SliderWithProductsProps } from "./type/interface";
import ProductCard from "../ProductCard/ProductCard";
import BaseSlider from "@/UI/Slider/BaseSlider";

function SliderWithProducts({title, watchAll, data}: SliderWithProductsProps) {
  console.log('data', data)
  return (
    <div className="slider-products lg:py-[80px] py-12">
      <div className="container px-4 mx-auto">
        <div className="slider-products__header lg:mb-16 mb-9 flex items-center justify-between md:flex-row flex-col md:gap-0 gap-4">
          <h3 className="m:text-size-h3 text-size-h2 uppercase text-accent-800 font-bold leading-130">{title}</h3>
          <Link to={watchAll} className="font-secondary underline text-size-body-3 leading-100 text-primary-600">дивитися всі</Link>
        </div>
        <div className="slider-products__body">
          <BaseSlider
            spaceBetween={24}
            navigation={true}
            slidesPerView={4}
            className="sliderWithProducts"
          >
            {data?.map(item => (
              <ProductCard item={item} key={item.id} />
            ))}
          </BaseSlider>
          
        </div>
      </div>
    </div>
  );
}

export default SliderWithProducts;