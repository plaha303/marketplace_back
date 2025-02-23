import MenuBottom from "./MenuBottom";
import MenuTop from "./MenuTop";

function Menu() {
	return (
		<div className="menu-block flex flex-col grow gap-y-[24px]  text-[20px]">
			<MenuTop />
			<MenuBottom />
		</div>
	);
}

export default Menu;


