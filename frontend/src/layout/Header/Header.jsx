import Menu from "../../components/Menu/Menu";
import Logo from "../../components/Logo/Logo";

function Header() {
	return (
		<div className="header bg-[#f1e4ff]">
			<div className="container mx-auto px-[15px]">
				<div className="flex flex-row justofy-center items-center gap-x-[24px] pt-[16px] pb-[16px]">
					<Logo/>
					<Menu/>
				</div>	
			</div>
		</div>
	);
}

export default Header;