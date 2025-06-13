import EmailIcon from "@/UI/Icons/EmailIcon";
import Logo from "../Logo/Logo";
import SocialLinks from "../SocialLinks/SocialLinks";
import PhoneIcon from "@/UI/Icons/PhoneIcon";
import RegionalSettings from "../ReginalSettings/RegionalSettings";
import { Button } from "@/UI/Button/Button";
import { Link } from "react-router";
import AppRoute from "@/routers/enums/routers-enums";

import PayMethods from "../PayMethods/PayMethods";
import { footerLinks1, footerLinks2, footerLinks3 } from "./type/interfaces";
import SearchBlock from "@/components/SearchBlock/SearchBlock";

function FooterTop(){ 
	return (
		<div className="w-full flex lg:flex-nowrap flex-wrap justify-between xl:gap-[67px] lg:gap-5">

			<div className="footer__left md:max-w-[276px] max-w-none md:mb-0 mb-9">
				<div className="md:mb-8 mb-4">
					<Logo />
					<div className="md:text-size-body-3 text-size-body-4  mt-4 leading-130">
						Найкраще для тих, хто цінує унікальність: ручна робота, ексклюзивн історії, теплі емоції.
					</div>
				</div>

				<div className="md:mb-8 mb-4">
					<div className="text-h-7 mb-4">Слідкуйте за нами:</div>
					<SocialLinks className="justify-start" />
				</div>

				<div className="md:mb-8">
					<div className="text-h-7 md:mb-4 mb-3">Контакти</div>
					<div className="flex items-center mb-2">
						<span className="mr-2 block">
							<EmailIcon className="text-snow" />
						</span>
						<a href="mailto:support@artlance.com" className="text-size-link-1 underline">support@artlance.com</a>
					</div>
					<div className="flex items-center mb-2">
						<span className="mr-2 block">
							<PhoneIcon className="text-snow" />
						</span>
						<a href="tel:+38 000 000 00 00" className="text-size-link-1">+38 000 000 00 00</a>
					</div>
				</div>
			</div>

			<div className="footer__middle lg:w-auto md:w-1/2 w-full md:mb-0 mb-6">
				<div className="footer__middle-block 2xl:columns-3 columns-2 xl:gap-[65px] lg:gap-5">
					{footerLinks1.map(item => (
						<Link to={item.path} key={item.id} className="text-size-link-1 text-snow block md:mb-6 mb-3 w-fit  md:whitespace-nowrap">{item.label}</Link>
					))}
					{footerLinks2.map(item => (
						<Link to={item.path} key={item.id} className="text-size-link-1 text-snow block md:mb-6 mb-3 w-fit md:whitespace-nowrap">{item.label}</Link>
					))}
					{footerLinks3.map(item => (
						<Link to={item.path} key={item.id} className="text-size-link-1 text-snow block md:mb-6 mb-3 w-fit md:whitespace-nowrap">{item.label}</Link>
					))}
				</div>
			</div>

			<div className="footer__right md:w-[375px] w-full">
				<div className="flex items-center gap-6 mb-8">
					<RegionalSettings />
					<Button asChild className="btn-secondary text-size-body-2 font-bold h-[56px] flex-1" size="lg">
						<Link to={AppRoute.LOGIN}>Вхід</Link>
					</Button>
				</div>
				<div className="mb-8 flex-1">
					<SearchBlock />
				</div>
				<div className="mb-8">
					<div className="text-h-7 font-bold mb-4">Підтримка платежів</div>
					<PayMethods />
				</div>
			</div>
		</div>
	)
}

export default FooterTop;

