import Logo from "../../components/Logo/Logo";

function FooterTop(){ 
    return (
        <div className="w-full flex lg:flex-row md:flex-col sm:flex-col flex-col justify-between">
            <div className="md:min-w-[160px] sm:min-w-full mr-[24px] flex items-start mb-4"> 
                <Logo/>
            </div>
            <div className="flex lg:flex-nowrap flex-wrap grow justify-between text-left">
                <div className="md:w-[180px] w-full flex flex-col md:gap-y-[16px] gap-y-[10px] mb-5">
                    <div className="lg:text-[24px] text-[19px] font-semibold md:leading-[36px] leading-1">
                        Компанія
                    </div>
                    <div className=" ">
                        <ul className="space-y-[8px]">
                            <li><a href="#" className="hover:underline block">Головна</a></li>
                            <li><a href="#" className="hover:underline block">Про нас</a></li>
                            <li><a href="#" className="hover:underline block">Послуги</a></li>
                            <li><a href="#" className="hover:underline block">Аукціони</a></li>
                            <li><a href="#" className="hover:underline block">Відгуки</a></li>
                            <li><a href="#" className="hover:underline block">Центр допомоги</a></li>
                        </ul>
                    </div>
                </div>
                <div className="md:w-[180px] w-full flex flex-col md:gap-y-[16px] gap-y-[10px] mb-5">
                    <div className="lg:text-[24px] text-[19px] font-semibold md:leading-[36px] leading-1">
                        Купити
                    </div>
                    <div>
                        <ul className="space-y-[8px]">
                            <li><a href="#" className="hover:underline">Оформлення заказу</a></li>
                            <li><a href="#" className="hover:underline">Оплата</a></li>
                            <li><a href="#" className="hover:underline">Доставка</a></li>
                            <li><a href="#" className="hover:underline">Взяти участь у аукціоні</a></li>
                        </ul>
                    </div>
                </div>
                <div className="md:w-[180px] w-full flex flex-col md:gap-y-[16px] gap-y-[10px] mb-5">
                    <div className="lg:text-[24px] text-[19px] font-semibold md:leading-[36px] leading-1">
                        Продати
                    </div>
                    <div>
                        <ul className="space-y-[8px]">
                            <li><a href="#" className="hover:underline">Реєстрація</a></li>
                            <li><a href="#" className="hover:underline">Оформлення особистого кабінета</a></li>
                            <li><a href="#" className="hover:underline">Рахунки</a></li>
                            <li><a href="#" className="hover:underline">Взяти участь у аукціоні</a></li>
                        </ul>
                    </div>
                </div>
                <div className="md:w-[232px] w-full flex flex-col md:gap-y-[24px] gap-y-[10px] mb-5">
                    <div className="lg:text-[24px] text-[19px] font-semibold md:leading-[36px] leading-1">
                        Форма оплати
                    </div>
                    <div className="flex flex-row lg:justify-between md:justify-start">
                        <div className="lg:mr-0 mr-4">
                            <img src="/img/master.svg" width={100} height={62}/>
                        </div>
                        <div>
                            <img src="/img/visa.svg" width={100} height={62}/>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default FooterTop;

