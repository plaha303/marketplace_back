import styled from '../Menu/Menu.module.css';


const siteLinks = [
	{name: 'Головна'},
	{name: 'Про нас'},
	{name: 'Послуги'},
	{name: 'Аукціони'},
	{name: 'Відгуки'},
	{name: 'Центр допомоги'}
] 
function MenuBottom() {
	return (
		<nav className="headerNav">
			<ul className="list-none hidden md:flex justify-center gap-x-[40px]">
				{siteLinks.map(link => (
					<li className="headerNav__item" key={link.name}><a href="#" className={`${styled.headerNav__link}`}>{link.name}</a></li>
				))}
			</ul>
		</nav>
	);
}

export default MenuBottom;