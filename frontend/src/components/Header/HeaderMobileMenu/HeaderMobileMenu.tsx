import RegionalSettings from "@/components/ReginalSettings/RegionalSettings";
import CloseIcon from "@/UI/Icons/CloseIcon";
import HeaderActions from "../HeaderActions/HeaderActions";
import MenuLinksSection from "@/components/Menu/MenuLinksSection/MenuLinksSection";
import MenuCatalog from "@/components/Menu/MenuCatalog";
import { HeaderMobileMenuProps } from "./type/interfaces";
import {AnimatePresence, motion} from "motion/react"
import ArrowDown from "@/UI/Icons/ArrowDown";
import { useEffect, useRef } from "react";
import HeaderTopPC from "../HeaderTop/HeaderTopPC";

function HeaderMobileMenu({handleOpenMenuCatalog, openMenuCatalog, handleCloseMobileMenu}: HeaderMobileMenuProps) {
  
  const menuTop = useRef<HTMLDivElement>(null);
  const menuBottom = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if(openMenuCatalog) {
      const topEl = menuTop.current;
      const bottomEl = menuBottom.current;

      if (topEl && bottomEl) {
        bottomEl.style.height = `calc(100% - ${topEl.offsetHeight}px)`;
      }
    }
  }, [openMenuCatalog])

  

  return (
    <div className='mobile-menu h-full overflow-y-auto'>
      <div className="mobile-menu bg-snow pb-5">
        <div className="mobile-menu__top bg-accent-600 flex items-center justify-between pr-4">
          <RegionalSettings />
          <span onClick={handleCloseMobileMenu}>
            <CloseIcon className="text-snow" />
          </span>
        </div>
        <div className="mobile-menu__middle bg-primary-800 py-2">
          <HeaderActions />
        </div>
        <div className="mobile-menu__bottom">
          <MenuLinksSection handleOpenMenuCatalog={handleOpenMenuCatalog} openMenuCatalog={openMenuCatalog} />

          <div className="help-links lg:p-0 px-2 py-3.5">
            <HeaderTopPC />
          </div>
        </div>

        <AnimatePresence>
          {openMenuCatalog && (
            <motion.div
              initial={{ opacity: 0, x: -285 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -285 }}
              transition={{ duration: 0.2 }}
              className="fixed z-[9999] top-0 w-[285px] h-full bg-snow pb-6"
            >
              <div className="mobileMenuCatalog__top" ref={menuTop}>
                <div className="text-size-body-3 flex items-center py-4 px-2.5 font-bold" onClick={handleOpenMenuCatalog}>
                  <span className="mr-2">
                    <ArrowDown className="text-primary-900 rotate-90" />
                  </span>
                  Назад
                </div>
                <div className="text-primary-400 text-sm py-2.5 px-3">
                  Виберіть зі списку:
                </div>
              </div>
              
              <div className="mobileMenuCatalog h-full overflow-auto" ref={menuBottom}>
                <MenuCatalog />
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}

export default HeaderMobileMenu;