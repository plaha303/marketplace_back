import { Button } from '@/UI/Button/Button';
import ArrowDown from '@/UI/Icons/ArrowDown';
import CatalogIcon from '@/UI/Icons/CatalogIcon';
import classNames from 'classnames';
import { Link } from 'react-router';
import menuLinks from '../MenuLinks';
import { MenuLinksSectionProps } from '../type/interfaces';
import styled from "./MenuLinksSection.module.scss"

function MenuLinksSection({handleOpenMenuCatalog, openMenuCatalog, buttonRef}: MenuLinksSectionProps) {
  
  return (
    <>
     <div className={classNames('xl:mr-9 lg:mr-7 lg:py-0 py-2', styled.menuCatalog__btn)}>
        <Button ref={buttonRef} className={classNames(
          `bg-transparent text-primary-900 hover:bg-transparent flex items-center 
          lg:px-5 min-w-[165px] min-h-[40px] border-1 border-transparent font-normal 
          shadow-none duration-500 rounded-[64px] py-2 !px-3 text-size-body-3
          `, 
          openMenuCatalog ? 'lg:shadow-custom1 border-1 lg:border-primary-100 duration-500' : ''
        )} 
          onClick={handleOpenMenuCatalog}
        >
          <CatalogIcon className="text-primary-900" />
          Категорія
          <ArrowDown className="text-primary-700 -rotate-90" />
        </Button>
      </div>
      <ul className={classNames("flex-1 flex lg:flex-row flex-col xl:gap-x-9 lg:gap-x-7 gap-2.5 lg:p-0 p-3.5", styled.menu__items)}>
        {menuLinks?.map(navLink => (
          <li key={navLink.id} className="menu__item">
            <Link to={navLink.path} className={classNames('menu__link block text-size-link-1 py-1.5 duration-500')}>{navLink.label}</Link>
          </li>
        ))}
      </ul> 
    </>
  );
}

export default MenuLinksSection;