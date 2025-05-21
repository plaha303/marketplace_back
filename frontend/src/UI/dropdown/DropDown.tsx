import { useState } from "react";
import Button from "../Button/Button";
import {DropDownProps} from "./type/interfaces"
import classNames from "classnames";
import { useClickOutside } from "@/helpers/useClickOutside";

function DropDown({buttonContent, classNameButton, classNameMenu, children}: DropDownProps) {
  const [isOpen, setIsOpen] = useState(false);

  const ref = useClickOutside<HTMLDivElement>(() => setIsOpen(false))

  function closeMenu() {
    setIsOpen(false)
  }

  return (
    <div ref={ref} className="dropdown relative">
      <Button className={classNameButton} onClick={() => setIsOpen(prev => !prev)}>
        {buttonContent}
      </Button>

      {isOpen && (<div className={classNames('dropdown-menu absolute right-0', classNameMenu)}>
        <div className="dropdown-menu__inner">
          {typeof children  === 'function' ? children(closeMenu) : children}
        </div>
      </div>)}
    </div>
  );
}

export default DropDown;