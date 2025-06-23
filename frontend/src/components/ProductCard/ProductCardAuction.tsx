import { Button } from "@/UI/Button/Button";
import { ProductCardAuctionProps } from "./types/interface";
import AuctionTimer from "../AuctionTimer/AuctionTimer";
import VideoCameraIcon from "@/assets/Icons/VideoCameraIcon.svg?react"

interface ProductCardAuctionComponentProps {
  product: ProductCardAuctionProps
}


function ProductCardAuction({product}: ProductCardAuctionComponentProps) {
  return (
    <div className="product-card__auction">
      <div className="product-card__auction-inner relative rounded-4xl">

        <div className="product-card__auction-top absolute w-[calc(100% - 32px)] top-4 left-4 right-4 flex justify-between items-center">
          <span className="product-card__auction-online label-onlineAuction inline-flex items-center md:gap-2 gap-1">
            <VideoCameraIcon />
            <span className="block font-secondary md:text-size-body-2 text-size-body-3 leading-100">Live аукціон</span>
          </span>
          <span className="product-card__auction-price label-onlineAuction-price font-secondary inline-flex items-center md:text-size-body-2 text-size-body-3 font-semibold leading-100">{product.price} грн</span>
        </div>

        <div className="product-card__auction-body">
          {product.images[0] && (
            <img src={product.images[0].image_url} alt="" className="rounded-4xl aspect-[224/261]" />
          )}
          
        </div>

        <div className="product-card__auction-footer absolute rounded-bl-4xl rounded-br-4xl bottom-0 w-full overflow-hidden">
          <div className="product-card__auction-title py-2 px-4  relative">
              <div className="absolute bg-snow-70 z-0 backdrop-blur-[2px] w-full h-full left-0 top-0" />
            <div className="text-accent-800 text-size-h6 font-bold leading-130 
            whitespace-nowrap overflow-hidden text-ellipsis relative z-3">{product.name}</div>
          </div>

          <div className="absolute rounded-bl-4xl rounded-br-4xl bg-accent-40 z-0 backdrop-blur-[2px] w-full h-[88px] left-0" />
          <div className="product-card__auction-actions  py-4 px-2 flex items-center gap-2 relative z-2">
            <div className="product-card__auction-timer">
              <AuctionTimer time={product.auction_end_time} />
            </div>
            <Button className="btn font-bold xl:text-size-body-2 text-size-body-3 flex-auto p-4">Зробити ставку</Button>
          </div>
        </div>

      </div>
    </div>
  );
}

export default ProductCardAuction;