import MenuCatalog from "./MenuCatalog";
import { AnimatePresence, motion } from "motion/react"
import MenuLinksSection from "./MenuLinksSection/MenuLinksSection";
import { MenuLinksSectionProps } from "./type/interfaces";
import { useClickOutside } from "@/utils/helpers/useClickOutside";
import { useRef } from "react";


function Menu({openMenuCatalog, handleOpenMenuCatalog}: MenuLinksSectionProps) {
  const buttonRef = useRef<HTMLButtonElement>(null);
  const catalogRef = useClickOutside<HTMLDivElement>(
    () => handleOpenMenuCatalog(),
    [buttonRef as React.RefObject<HTMLElement>]
  );
  return (
    <nav className="menu border-b-1 border-primary-100 py-7">
      <div className="container mx-auto px-4">
        <div className=" menu__inner relative">
          <div className="flex items-center">
            <MenuLinksSection handleOpenMenuCatalog={handleOpenMenuCatalog} openMenuCatalog={openMenuCatalog} buttonRef={buttonRef} />
          </div>

          <AnimatePresence>
            {openMenuCatalog && (
                <motion.div
                  key="catalogMenu"
                  ref={catalogRef}
                  initial={{ opacity: 0, y: -5 }}
                  animate={{ opacity: 1, y: 5 }}
                  exit={{ opacity: 0, y: -5 }}
                  transition={{ duration: 0.25 }}
                >
                  <MenuCatalog />
                </motion.div>
              )
            }
          </AnimatePresence>
        </div>
      </div>
    </nav>
  );
}

export default Menu;