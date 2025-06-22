import { Button } from "@/UI/Button/Button";


function ProductCardAuction() {
  return (
    <div className="product-card__auction">
      <div className="product-card__auction-inner">
        <div className="product-card__auction-top">
          <span className="product-card__auction-online"></span>
          <span className="product-card__auction-price"></span>
        </div>
        <div className="product-card__auction-body">
          <img src="" alt="" />
        </div>
        <div className="product-card__auction-footer">
          <div className="product-card__auction-title"></div>
          <div className="product-card__auction-actions">
            <div className="product-card__auction-timer"></div>
            <Button className="btn-primary">Зробити ставку</Button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ProductCardAuction;