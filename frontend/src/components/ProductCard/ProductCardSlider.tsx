import { Button } from "@/UI/Button/Button";
import { Rating } from "react-simple-star-rating";
import { Link } from "react-router";
import { useCategoryHref } from "@/utils/helpers/useCategoryHref";
import { ProductDTO } from "@/utils/packages/hitsProducts/type/interface";

import Heart from '@/assets/Icons/Heart.svg?react'
import ShoppingCart from '@/assets/Icons/ShoppingCart.svg?react'
import Tote from '@/assets/Icons/Tote.svg?react'

interface ProductCardProps {
  item: ProductDTO
}

function ProductCard({item}: ProductCardProps) {
  const categoryHref = useCategoryHref(item.category);

  return (
    <div className="product-cart h-full">
      <div className="product-cart__inner rounded-4xl shadow-custom1 h-full flex flex-col">
        <div className="product-cart__top relative">
          <span className="product-cart__label"></span>
          <Button type="button" variant="default" className="btn rounded-full w-[56px] h-[56px] p-0 absolute top-4 right-4">
            <Heart className="text-snow" />
          </Button>
          <div className="product-cart__top-img">

            {item.images?.[0] && (
              <img
                src={item.images[0].image_url}
                alt=""
                className="product-cart__img rounded-t-4xl"
                key={item.images[0].id}
              />
            )}
            
          </div>
        </div>
        <div className="product-cart__body p-6 flex-1 flex flex-col">

          <div className="product-cart__body-top flex-1">
            <div className="product-cart__rating mb-2">
              <Rating readonly initialValue={item.rating} fillColor="#A0864D" className="flex" size={20} SVGclassName="inline" />
              <span className="text-size-body-3 text-primary-600 leading-130 font-secondary">({item.reviews_count})</span>
            </div>
            <Link to={`${categoryHref}/${item.product_href}`} className="product-cart__title text-size-h6 font-bold leading-130 mb-2">{item.name}</Link>
          </div>
            
          <div className="product-cart__body-bottom">
            <div className="flex items-center justify-between">
              <div className="product-cart__price flex">
                {item.discount_price && (
                  <span className="mr-2 font-secondary text-primary-600 text-size-body-1 leading-130 line-through">{item.discount_price}</span>
                )}
                <span className="font-secondary text-accent-800 text-size-body-1 leading-130">{item.price}</span>
              </div>

              <Button type="button" variant="ghost" className="p-[10px]">
                <ShoppingCart className="text-accent-700"/>
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ProductCard;