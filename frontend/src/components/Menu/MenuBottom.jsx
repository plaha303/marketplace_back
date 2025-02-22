import styled from '../Menu/Menu.module.css';

function MenuBottom() {
	return (
		<nav>
			<ul className={`liist-none flex justify-center gap-x-[40px] mt-[24px]`}>
				<li><a href="#">Головна</a></li>
				<li><a href="#">Про нас</a></li>
				<li><a href="#">Послуги</a></li>
				<li><a href="#">Аукціони</a></li>
				<li><a href="#">Відгуки</a></li>
				<li><a href="#">Центр допомоги</a></li>
			</ul>
		</nav>
	);
}

export default MenuBottom;