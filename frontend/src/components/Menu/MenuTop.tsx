import { useState } from 'react';
import { openAuthModal } from '../../store/authModalSlice';

import styled from '../Menu/Menu.module.css';
import DropDown from '../../UI/dropdown/DropDown';
import { RootState } from '../../store/store';
import { useAppDispatch, useAppSelector } from '../../store/hooks/hooks';



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
	const isCodeSent = useAppSelector((state: RootState) => state.authModal.isCodeSent);

	const dispatch = useAppDispatch();
	const [selectedDropdown, setSelectedDropdown] = useState({
		currencies: '₴',
		languages: 'ua',
	});

	function selectItem(itemName: string, dropdownKey: string) {
		setSelectedDropdown((prev) => ({
			...prev,
			[dropdownKey]: itemName,
		}));
	}

	function handleModalShow() {
		if(isCodeSent) {
			dispatch(openAuthModal('EmailConfirm'))
		} else {
			dispatch(openAuthModal('LogIn'))
		}
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
				<div className={`mx-[24px] flex justify-center items-center grow`}>
					<label className={`w-full input flex justify-between items-center gap-2 rounded-[50px] bg-transparent ${styled.searchBlock}`}>
						<input type="text" className="w-full" placeholder="Шукаю..." />
						<div className="h-[18px] w-[18px]">
							<svg width="18" height="18" viewBox="0 0 18 18" fill="none" xmlns="http://www.w3.org/2000/svg">
								<path d="M16.6 18L10.3 11.7C9.8 12.1 9.225 12.4167 8.575 12.65C7.925 12.8833 7.23333 13 6.5 13C4.68333 13 3.14583 12.3708 1.8875 11.1125C0.629167 9.85417 0 8.31667 0 6.5C0 4.68333 0.629167 3.14583 1.8875 1.8875C3.14583 0.629167 4.68333 0 6.5 0C8.31667 0 9.85417 0.629167 11.1125 1.8875C12.3708 3.14583 13 4.68333 13 6.5C13 7.23333 12.8833 7.925 12.65 8.575C12.4167 9.225 12.1 9.8 11.7 10.3L18 16.6L16.6 18ZM6.5 11C7.75 11 8.8125 10.5625 9.6875 9.6875C10.5625 8.8125 11 7.75 11 6.5C11 5.25 10.5625 4.1875 9.6875 3.3125C8.8125 2.4375 7.75 2 6.5 2C5.25 2 4.1875 2.4375 3.3125 3.3125C2.4375 4.1875 2 5.25 2 6.5C2 7.75 2.4375 8.8125 3.3125 9.6875C4.1875 10.5625 5.25 11 6.5 11Z" fill="#01060B" />
							</svg>
						</div>
					</label>
				</div>
				<div className={`flex gap-x-[16px] items-center`}>
					<DropDown
						current={selectedDropdown.languages}
						list={languages}
						selectItem={(itemName:string) => selectItem(itemName, "languages")}
						classBlock={`${styled.dropDownBtn} ${styled.languagesBtn}`}
					/>
					<DropDown
						current={selectedDropdown.currencies}
						list={currencies}
						selectItem={(itemName: string) => selectItem(itemName, "currencies")}
						classBlock={`${styled.dropDownBtn} ${styled.currenciesBtn}`}
					/>
				
				<button type="button" onClick={() => handleModalShow()} className={`flex items-center ${styled.headerBtn__action}`}>
					<span className={`icon me-2 ${styled.iconUser}`}></span>
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
		</div>
	);
}

export default MenuTop;
