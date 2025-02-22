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
		<div className={`h-[46px] flex justify-between items-center `}>
				<div className={`flex justify-center items-center`}>
					<button type="button" className={`flex items-center ${styled.headerBtn__action}`}> 
						<span className={`icon me-2 ${styled.iconCatalog}`}></span>
						Каталог
					</button>
					{/* <DropDown  
					/> */}
				</div>
				<div className={`px-[24px] flex justify-center items-center grow`}>
					<label className="w-full input input-bordered flex justify-center items-center gap-2 rounded-[50px] p-none">
						<input type="text" className="bg-none" placeholder="Шукаю..." />
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
				<div className={`flex gap-x-[16px] items-center`}>
					<DropDown
						current={selectedDropdown.languages}
						list={languages}
						selectItem={(itemName) => selectItem(itemName, "languages")}
					/>
					<DropDown
						current={selectedDropdown.currencies}
						list={currencies}
						selectItem={(itemName) => selectItem(itemName, "currencies")}
					/>
				
					<button type="button" onClick={handleOpenLogin} className={`flex items-center ${styled.headerBtn__action}`}>
						<span className={`icon me-2 ${styled.iconUser} ${styled.headerBtn__action}`}></span>
						Увійти
					</button>

					<button type="button" className={`flex items-center ${styled.headerBtn__action}`}>
						<span className={`icon me-2 ${styled.iconFavorite}`}></span>
						Обране
					</button>

					<button type="button" className={`flex items-center ${styled.headerBtn__action}`}>
						<span className={`icon me-2 ${styled.iconBasket}`}></span>
						Кошик
					</button>
				</div>
			{isOpenLogIn && <LogIn/>}
		</div>
	);
}

export default MenuTop;
