import Menu from "../../components/Menu/Menu";
import Logo from "../../components/Logo/Logo"

function Header() {
	return (
		<div className="header bg-[#E4CAFF]">
			<div className="container max-w-screen-xl mx-auto gap-x-[24px] 
			flex flex-row justofy-center items-center px-[60px] md:px-[30px] sm:px-[5px]">
				<Logo/>
				<Menu/>
			</div>
		</div>
	);
}

export default Header;