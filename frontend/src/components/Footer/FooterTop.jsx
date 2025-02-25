import Logo from "../../components/Logo/Logo";
import VisaImage from "../../../public/img/visa_method_card_payment_icon.svg";
import MasterImage from "../../../public/img/master_method_card_payment_icon.svg";

function FooterTop(){ 
    return (
        <div className="w-full flex lg:flex-row md:flex-row sm:flex-row flex-col justify-between border-b border-white pb-[24px]">
            <div className="min-w-[160px] mr-[24px] flex items-start"> 
                <Logo/>
            </div>
            <div className="flex lg:flex-nowrap flex-wrap grow justify-between lg:gap-y-[116px] md:gap-y-[116px] text-left gap-4">
                <div className="w-[180px] flex flex-col gap-y-[16px]">
                    <div className="text-[24px] font-semibold leading-[36px]">
                        Компанія
                    </div>
                    <div className=" ">
                        <ul className="space-y-[8px]">
                            <li><a href="#">Головна</a></li>
                            <li><a href="#">Про нас</a></li>
                            <li><a href="#">Послуги</a></li>
                            <li><a href="#">Аукціони</a></li>
                            <li><a href="#">Відгуки</a></li>
                            <li><a href="#">Центр допомоги</a></li>
                        </ul>
                    </div>
                </div>
                <div className="w-[180px] flex flex-col gap-y-[16px]">
                    <div className="text-[24px] font-semibold leading-[36px]">
                        Купити
                    </div>
                    <div>
                        <ul className="space-y-[8px]">
                            <li><a href="#">Оформлення заказу</a></li>
                            <li><a href="#">Оплата</a></li>
                            <li><a href="#">Доставка</a></li>
                            <li><a href="#">Взяти участь у аукціоні</a></li>
                        </ul>
                    </div>
                </div>
                <div className="w-[180px] flex flex-col gap-y-[16px]">
                    <div className="text-[24px] font-semibold leading-[36px]">
                        Продати
                    </div>
                    <div>
                        <ul className="space-y-[8px]">
                            <li><a href="#">Реєстрація</a></li>
                            <li><a href="#">Оформлення особистого кабінета</a></li>
                            <li><a href="#">Рахунки</a></li>
                            <li><a href="#">Взяти участь у аукціоні</a></li>
                        </ul>
                    </div>
                </div>
                <div className="w-[232px] flex flex-col gap-y-[24px] ">
                    <div className="text-[24px] font-semibold leading-[36px]">
                        Форма оплати
                    </div>
                    <div className="flex flex-row justify-between">
                        <div>
                            <img src={MasterImage} width={100} height={62}/>
                        </div>
                        <div>
                            <img src={VisaImage} width={100} height={62}/>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default FooterTop;

