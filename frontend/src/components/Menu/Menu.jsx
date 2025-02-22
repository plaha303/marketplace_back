import MenuBottom from "./MenuBottom";
import MenuTop from "./MenuTop";

function Menu() {
	return (
		<div className="menu-block flex flex-col gap-y-[24px] pt-[16px] pb-[16px]">
			<MenuTop />
			<MenuBottom />
		</div>
	);
}

export default Menu;