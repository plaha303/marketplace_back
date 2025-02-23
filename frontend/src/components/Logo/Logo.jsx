import {Link} from "react-router"

function Logo() {
	return (
		<Link to="/"
			className={`max-w-[200px]`}
		>
			<img src="/img/Logo.svg" alt="Logo" className="size-full" />
		</Link>
	);
}

export default Logo;
