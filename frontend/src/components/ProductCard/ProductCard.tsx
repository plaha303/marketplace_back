import { Button } from "@/UI/Button/Button";

import Heart from '@/assets/Icons/Heart.svg?react'
import ShoppingCart from '@/assets/Icons/ShoppingCart.svg?react'
import Eye from '@/assets/Icons/Eye.svg?react'
import { Rating } from "react-simple-star-rating";

function ProductCard() {
  return (
    <div className="product-cart">
      <div className="product-cart__inner">
        <div className="product-cart__top relative">
          <span className="product-cart__label"></span>
          <div className="product-cart__top-img">
            <img src="" alt="" className="product-cart__img" />
          </div>
          <div className="product-cart__top-actions">
            <div className="flex items-center gap-2">
              <Button type="button" variant="default" className="btn rounded-full w-[56px] h-[56px] p-0">
                <Heart />
              </Button>
              <Button type="button" variant="default" className="btn rounded-full w-[56px] h-[56px] p-0">
                <ShoppingCart />
              </Button>
              <Button type="button" variant="default" className="btn rounded-full w-[56px] h-[56px] p-0">
                <Eye />
              </Button>
            </div>
          </div>
        </div>
        <div className="product-cart__body">
          <div className="product-cart__rating mb-2">
            <Rating initialValue={4} fillColor="#A0864D" />
            <span className="text-size-body-3 text-primary-600 leading-130 font-secondary">(56,767)</span>
          </div>
          <div className="product-cart__title text-size-h6 font-bold leading-130 mb-2"></div>
          <div className="product-cart__price flex">
            <span className="mr-2 font-secondary text-primary-600 text-size-body-1 leading-130 line-through"></span>
            <span className="font-secondary text-accent-800 text-size-body-1 leading-130"></span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ProductCard;