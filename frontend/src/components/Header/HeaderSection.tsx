import { useEffect, useState } from "react";
import Menu from "../Menu/Menu";
import HeaderBottom from "./HeaderBottom/HeaderBottom";
import HeaderTop from "./HeaderTop/HeaderTop";
import { useMediaQuery } from "react-responsive";
import { AnimatePresence, motion } from "motion/react"
import HeaderMobileMenu from "./HeaderMobileMenu/HeaderMobileMenu";
import UserMenu from "../UserMenu/UserMenu";

function HeaderSection() {
	const [activeHamburger, setActiveHamburger] = useState(false);
	const [openMenuCatalog, setOpenMenuCatalog] = useState(false);
	const [userMenu, setUserMenu] = useState(false);

  function handleOpenMenuCatalog() {
    setOpenMenuCatalog(prev => !prev)
  }

	function handleOpenUserMenu() {
		setUserMenu(prev => !prev)
	}
	
	function handleCloseMobileMenu() {
    setActiveHamburger(false)
		setOpenMenuCatalog(false)
		setUserMenu(false)
  }

	const isWidth1023 = useMediaQuery({query: '(max-width: 1023px)'});

	useEffect(() => {
		if(activeHamburger || userMenu) {
			document.body.style.overflow = 'hidden';
			document.body.style.paddingRight = '16px'
		} else {
			document.body.style.overflow = '';
			document.body.style.paddingRight = '0px'
		}
	}, [activeHamburger, userMenu])

	return (
		<div className="menu-block">
			<HeaderTop />
			<HeaderBottom setActiveHamburger={setActiveHamburger} activeHamburger={activeHamburger} handleOpenUserMenu={handleOpenUserMenu} />

			{!isWidth1023 && (<Menu handleOpenMenuCatalog={handleOpenMenuCatalog} openMenuCatalog={openMenuCatalog} />)}

			<AnimatePresence>
				{activeHamburger && (<motion.div
					key="sidebar"
					initial={{ opacity: 0, x: -285 }}
					animate={{ opacity: 1, x: 0 }}
					exit={{ opacity: 0, x: -285 }}
					transition={{ duration: 0.25 }}
					className="fixed z-[10] top-0 w-[285px] h-full"
				>
					<HeaderMobileMenu handleOpenMenuCatalog={handleOpenMenuCatalog} openMenuCatalog={openMenuCatalog} handleCloseMobileMenu={handleCloseMobileMenu} handleOpenUserMenu={handleOpenUserMenu} />
				</motion.div>)}
			</AnimatePresence>
				
			<AnimatePresence>
					{userMenu && (
					<motion.div
						key="userSideBar"
						initial={{ opacity: 0, x: 355 }}
						animate={{ opacity: 1, x: 0 }}
						exit={{ opacity: 0, x: 355 }}
						transition={{ duration: 0.25 }}
						className="fixed z-[10] top-0 w-[355px] right-0 h-full"
					>
						<UserMenu />
					</motion.div>
				)}
			</AnimatePresence>

			{(activeHamburger || userMenu) && (<div className="overlay" onClick={handleCloseMobileMenu}></div>)}

		</div>
	);
}

export default HeaderSection;