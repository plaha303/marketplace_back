import LogoIcon from "@/UI/Icons/LogoIcon";
import LogoTextIcon from "@/UI/Icons/LogoTextIcon";
import {Link} from "react-router"

function Logo() {
	return (
		<Link to="/"
			className="max-w-[276px] flex items-center"
		>
			<div className="logo-img max-w-[40px] flex-[40px] me-2">
				<LogoIcon color="#A0864D" />
			</div>
			<span className="logo-text">
				<LogoTextIcon color="#FCFCFC" />
			</span>
		</Link>
	);
}

export default Logo;