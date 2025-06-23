import SliderAuction from "../SliderAuction/SliderAuction";
import AuctionBlockContent from "./AuctionBlockContent";

function AuctionBlock() {
  return (
    <div className="auction-block pattern-bg lg:py-[80px] py-12">
      <div className="container px-4 mx-auto">
        <div className="auction-block__inner flex justify-between xl:flex-row flex-col xl:gap-4 gap-9 md:overflow-hidden">
          <div className="auction-block__left xl:max-w-[565px] p-1.5">
            <AuctionBlockContent />
          </div>
          <div className="auction-block__right xl:max-w-[685px]">
            <SliderAuction />
          </div>
        </div>
      </div>
    </div>
  );
}

export default AuctionBlock;