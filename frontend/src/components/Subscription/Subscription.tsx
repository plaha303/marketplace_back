import { Button } from "@/UI/Button/Button";
import BaseInput from "@/UI/Input/BaseInput";
import SocialLinks from "../SocialLinks/SocialLinks";
import SubscriptionImg from '@/assets/SubscriptionImg.png'

function Subscription() {
  return (
    <div className="subscription pattern-bg">
      <div className="container px-4 mx-auto">
        <div className="subscription__inner flex lg:flex-row flex-col items-end  xl:gap-6">
          <div className="special-offer__left lg:max-w-[565px] xl:py-[84px] lg:py-12 pt-12 lg:mb-0 mb-9">
            <div className="special-offer__content md:p-12 p-4 rounded-4xl shadow-custom2 bg-snow-70">
              <h3 className="special-offer__content-title uppercase lg:text-size-h3 text-size-h2 leading-130 text-accent-800 md:mb-10 mb-4 font-bold">
                Стань частиною світу унікальних речей!
              </h3>
              <div className="special-offer__content-text md:text-size-body-1 text-size-body-3 md:mb-[56px] mb-8 font-secondary">
                <p className="leading-130">
                  Отримуй першим новини про ексклюзивні знижки, нові колекції та хендмейд-аукціони!
                </p>
              </div>

              <div className="subscription__form md:mb-[56px] mb-8">
                <form>
                  <div className="mb-6">
                    <BaseInput placeholder="Введіть e-mail"/>
                  </div>
                  <Button type="submit" variant="default" className="w-full font-secondary text-size-body-2 font-bold leading-100 h-14">Підписатися</Button>
                </form>
              </div>

              <div className="social-block">
                <div className="mb-4 text-size-body-3">Слідкуйте за нами:</div>
                <SocialLinks colorIcon="text-accent-700" className="justify-start" />
              </div>

            </div>
          </div>

          <div className="special-offer__right flex-1">
            <img src={SubscriptionImg} alt="Subscription img" />
          </div>
        </div>
      </div>
    </div>
  );
}

export default Subscription;