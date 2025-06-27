import { Button } from "@/UI/Button/Button";
import { Link } from "react-router";
import SpecialOfferImg from "@/assets/specialOffer.png"

function SpecialOffers() {
  return (
    <div className="special-offers pattern-bg">
      <div className="container px-4 mx-auto">
        <div className="special-offer__inner flex items-end lg:flex-row flex-col xl:gap-6">
          <div className="special-offer__left lg:max-w-[565px] xl:py-[84px] lg:py-12 pt-12 lg:mb-0 mb-9">
            <div className="special-offer__content md:p-12 p-4 rounded-4xl shadow-custom2 bg-snow-70">
              <h3 className="special-offer__content-title uppercase lg:text-size-h3 text-size-h2 leading-130 text-accent-800 md:mb-10 mb-4 font-bold">
                Зроби вигідну покупку вже сьогодні!!
              </h3>
              <div className="special-offer__content-text md:text-size-body-1 text-size-body-3 md:mb-[56px] mb-8 font-secondary">
                <p className="leading-130">
                  Знижки до -40% на унікальні хендмейд-товари!
                  Встигніть придбати унікальні вироби за спеціальною ціною!
                </p>
                <p className="leading-130">
                  Кожен товар створений з душею та майстерністю, щоб зробити твій простір особливим.
                </p>
              </div>
              <div className="special-offer__content-footer md:max-w-[300px]">
                <Button asChild variant="default" className="btn text-snow font-bold font-secondary leading-100 md:text-size-body-2 text-size-body-3 md:h-14 h-11 md:w-full p-4">
                  <Link to="/">Спеціальні пропозиції</Link>
                </Button>
              </div>
            </div>
          </div>
          <div className="special-offer__right flex-1">
            <img src={SpecialOfferImg} alt="Special offer" />
          </div>
        </div>
      </div>
    </div>
  );
}

export default SpecialOffers;