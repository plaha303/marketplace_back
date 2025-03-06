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
		<nav className="headerNav flex lg:hidden">
			<ul className="list-none flex flex-col justify-center gap-y-[10px]">
				{siteLinks.map(link => (
					<li className="headerNav__item" key={link.name}><a href="#" className={`${styled.headerNav__link}`}>{link.name}</a></li>
				))}
			</ul>
		</nav>
	);
}

export default MenuBottom;