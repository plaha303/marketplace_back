import React, { useState} from 'react'
import Menu from "../../components/Menu/Menu";
import Logo from "../../components/Logo/Logo";
import BurgerButton from '../../components/Menu/BurgerButton/BurgerButton';
import MenuMobile from "../../components/Menu/MenuMobile";
import styled from "../../components/Menu/Menu.module.css"


function Header() {

	const [isButtonClicked, setIsButtonClicked] = useState(false);
	const [count, setCount] = useState(0);

	const handleButtonClick = () => {  
		setIsButtonClicked(!isButtonClicked);

	//   setCount(count + 1);
	//   const isEven = count % 2 === 0;
	//   if (isEven) setIsButtonClicked(!isButtonClicked);

	};
	
	return (
		<div className="header bg-[#f1e4ff] relative">
			<div className="xl:container lg:container xl:mx-auto lg:mx-auto px-[15px]">
				<div className="flex flex-row justofy-center items-center lg:gap-x-[24px] pt-[16px] pb-[16px]">
					<Logo/>
					<Menu/>
					<BurgerButton onButtonClick={handleButtonClick}/>
				</div>	
			</div>
			<MenuMobile isButtonClicked={isButtonClicked} onButtonClick={handleButtonClick}/>
		</div>
	);
}

export default Header;