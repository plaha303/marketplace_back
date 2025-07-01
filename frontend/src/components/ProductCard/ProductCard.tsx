import { Button } from "@/UI/Button/Button";

import Heart from '@/assets/Icons/Heart.svg?react'
import ShoppingCart from '@/assets/Icons/ShoppingCart.svg?react'
import Eye from '@/assets/Icons/Eye.svg?react'
import { Rating } from "react-simple-star-rating";

import style from './ProductCard.module.scss'
import { Link } from "react-router";
import { useCategoryHref } from "@/utils/helpers/useCategoryHref";
import { ProductDTO } from "@/utils/packages/hitsProducts/type/interface";

interface ProductCardProps {
  item: ProductDTO
}

function ProductCard({item}: ProductCardProps) {
  const categoryHref = useCategoryHref(item.category);

  return (
    <div className="product-cart">
      <div className="product-cart__inner rounded-4xl shadow-custom1">
        <div className="product-cart__top relative">
          <span className="product-cart__label"></span>
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
          <div className={`${style.productCart__topActions}`}>
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
        <div className="product-cart__body p-6">
          <div className="product-cart__rating mb-2">
            <Rating readonly initialValue={item.rating} fillColor="#A0864D" className="flex" size={20} SVGclassName="inline" />
            <span className="text-size-body-3 text-primary-600 leading-130 font-secondary">({item.reviews_count})</span>
          </div>
          <Link to={`${categoryHref}/${item.product_href}`} className="product-cart__title text-size-h6 font-bold leading-130 mb-2">{item.name}</Link>
          <div className="product-cart__price flex">
            {item.discount_price && (
              <span className="mr-2 font-secondary text-primary-600 text-size-body-1 leading-130 line-through">{item.discount_price}</span>
            )}
            
            <span className="font-secondary text-accent-800 text-size-body-1 leading-130">{item.price}</span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ProductCard;