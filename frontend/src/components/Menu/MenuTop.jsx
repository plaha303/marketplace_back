import { useState } from 'react';
import styled from '../Menu/Menu.module.css';
import DropDown from '../../UI/dropdown/dropdown';
import LogIn from '../LogIn/LogIn';

const currencies = [
	{ id: '1', name: '₴' },
	{ id: '2', name: '$' },
	{ id: '3', name: '€' },
];

const languages = [
	{ id: '1', name: 'ua' },
	{ id: '2', name: 'us' },
];

function MenuTop() {
	const [isOpenLogIn, setIsOpenLogIn] = useState(false);
	const [selectedDropdown, setSelectedDropdown] = useState({
		currencies: '₴',
		languages: 'ua',
	});

	function selectItem(itemName, dropdownKey) {
		setSelectedDropdown((prev) => ({
			...prev,
			[dropdownKey]: itemName,
		}));
	}

	function handleOpenLogin() {
		setIsOpenLogIn(true);
	}

	return (
		<div style={menuTopItems}>
			<div style={leftSideMenu}>
				<div style={logo}>logo</div>
				<button type="button" style={catalog}> 
					<span style={iconCatalog}></span>
					Каталог
				</button>
				{/* <DropDown
					нужно ли создавтаь отдельный компнонет для выпадающего каталога? 
				/> */}
			</div>
			<div style={middleSideMenu}>
				<label className="input input-bordered flex items-center gap-2">
					<input type="text" className="grow" placeholder="Шукаю..." />
					<svg
						xmlns="http://www.w3.org/2000/svg"
						viewBox="0 0 16 16"
						fill="currentColor"
						className="h-4 w-4 opacity-70"
					>
						<path
							fillRule="evenodd"
							d="M9.965 11.026a5 5 0 1 1 1.06-1.06l2.755 2.754a.75.75 0 1 1-1.06 1.06l-2.755-2.754ZM10.5 7a3.5 3.5 0 1 1-7 0 3.5 3.5 0 0 1 7 0Z"
							clipRule="evenodd"
						/>
					</svg>
				</label>
			</div>
			<div style={rightSideMenu}>
				<DropDown
					current={selectedDropdown.currencies}
					list={currencies}
					selectItem={(itemName) => selectItem(itemName, "currencies")}
				/>
				<DropDown
					current={selectedDropdown.languages}
					list={languages}
					selectItem={(itemName) => selectItem(itemName, "languages")}
				/>
				
				<button type="button" onClick={handleOpenLogin} className={`flex flex-col items-center ${styled.headerBtn__action}`}>
					<span className={`icon me-2 ${styled.iconUser} ${styled.headerBtn__action}`}></span>
					Увійти
				</button>

				<button type="button" className={`flex flex-col items-center ${styled.headerBtn__action}`}>
					<span className={`icon me-2 ${styled.iconFavorite}`}></span>
					Обране
				</button>

				<button type="button" className={`flex flex-col items-center ${styled.headerBtn__action}`}>
					<span className={`icon me-2 ${styled.iconBasket}`}></span>
					Кошик
				</button>
			</div>

			{isOpenLogIn && <LogIn/>}
		</div>
	);
}

const menuTopItems = {
	height: '56px',
	display: 'flex',
	justifyContent: 'center',
	alignItems: 'center',
	marginTop: '16px'
}
const logo = {
	width: '90px',
	height: '56px',
	display: 'flex',
	justifyContent: 'center',
	alignItems: 'center',
	backgroundColor: 'gray'
}
const catalog = {
	width: '96px',
	height: '34px',
	display: 'flex',
	justifyContent: 'center',
	alignItems: 'center',
	columnGap: '8px',
	margin: '0 auto',
	borderRadius: '8px',
	backgroundColor: 'black',
	border: '1px solid gray',
	fontSize: '12px',
	color: 'white'
}
const iconCatalog = {
	width: '16px',
	height: '16px',
	background: 'url("/img/icons/chevron-double-down.svg") no-repeat'
  }
const leftSideMenu = {
	height: "100%",
	flexGrow: '1',
	display: 'flex',
	justifyContent: 'space-between',
	alignItems: 'center'
}
const middleSideMenu = {
	width: '569px',
	paddingRight: '40px'
}
const rightSideMenu ={
	display: 'flex',
	columnGap: '16px',
	alignItems: 'center'
}

export default MenuTop;
