import LogoIcon from "@/UI/Icons/LogoIcon";
import {Link} from "react-router"

function Logo() {
	return (
		<Link to="/"
			className={`max-w-[200px]`}
		>
			<LogoIcon color="#A0864D" />
			<span className="logo-text text-h2">ArtLance</span>
		</Link>
	);
}

export default Logo;