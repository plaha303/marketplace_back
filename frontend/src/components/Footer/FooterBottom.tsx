import { Link } from "react-router";
import { footerBottomLinks } from "./type/interfaces";
import style from "./Footer.module.scss"

function FooterBottom() {
	return (
		<div className="md:mt-6 md:py-6 pt-1 pb-6 m-0">
			<div className="flex items-center lg:justify-between justify-center lg:flex-nowrap flex-wrap lg:flex-row flex-col">
				<div className="flex items-center lg:mb-0 mb-6 md:flex-row flex-col md:gap-0 gap-3">
					{footerBottomLinks.map(item => (
						<Link to={item.path} key={item.id} className={`${style.footerBottom__link} text-size-link-1`}>{item.label}</Link>
					))}
				</div>

				<div className="flex items-center">
					<div className={`${style.footer__copyright} text-size-link-1`}>
						&copy; 2025 - Artlance 
					</div>
					<div >Всі права захищено</div>
				</div>
			</div>
		</div>
	);
}

export default FooterBottom;
