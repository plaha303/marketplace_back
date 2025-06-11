import { useEffect, useState } from "react";
import Menu from "../Menu/Menu";
import HeaderBottom from "./HeaderBottom/HeaderBottom";
import HeaderTop from "./HeaderTop/HeaderTop";
import { useMediaQuery } from "react-responsive";
import { AnimatePresence, motion } from "motion/react"
import HeaderMobileMenu from "./HeaderMobileMenu/HeaderMobileMenu";
import { useClickOutside } from "@/utils/helpers/useClickOutside";


function HeaderSection() {
	const [activeHamburger, setActiveHamburger] = useState(false);
	const [openMenuCatalog, setOpenMenuCatalog] = useState(false);

  function handleOpenMenuCatalog() {
    setOpenMenuCatalog(prev => !prev)
  }

	function handleCloseMobileMenu() {
    setActiveHamburger(prev => !prev)
		setOpenMenuCatalog(false)
  }

	const ref = useClickOutside<HTMLDivElement>(() => handleCloseMobileMenu())

	const isWidth1023 = useMediaQuery({query: '(max-width: 1023px)'});

	useEffect(() => {
		if(activeHamburger) {
			document.body.style.overflow = 'hidden';
		} else {
			document.body.style.overflow = '';
		}
	}, [activeHamburger])

	return (
		<div className="menu-block">
			<HeaderTop />
			<HeaderBottom setActiveHamburger={setActiveHamburger} activeHamburger={activeHamburger} />

			{!isWidth1023 && (<Menu handleOpenMenuCatalog={handleOpenMenuCatalog} openMenuCatalog={openMenuCatalog} />)}

			<AnimatePresence>
				{activeHamburger && (<motion.div
					ref={ref}
					key="sidebar"
					initial={{ opacity: 0, x: -285 }}
					animate={{ opacity: 1, x: 0 }}
					exit={{ opacity: 0, x: -285 }}
					transition={{ duration: 0.25 }}
					className="fixed z-[9] top-0 w-[285px] h-full"
				>
					<HeaderMobileMenu handleOpenMenuCatalog={handleOpenMenuCatalog} openMenuCatalog={openMenuCatalog} handleCloseMobileMenu={handleCloseMobileMenu} />
				</motion.div>)}
			</AnimatePresence>

			{activeHamburger && (<div className="overlay"></div>)}

		</div>
	);
}

export default HeaderSection;