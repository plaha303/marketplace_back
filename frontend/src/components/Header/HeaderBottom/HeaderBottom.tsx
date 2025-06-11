import Logo from "@/components/Logo/Logo";
import RegionalSettings from "@/components/ReginalSettings/RegionalSettings";
import SearchBlock from "@/components/SearchBlock/SearchBlock";
import HeaderActions from "../HeaderActions/HeaderActions";
import { useMediaQuery } from "react-responsive";
import classNames from "classnames";
import { HeaderBottomProps } from "./type/interfaces";

function HeaderBottom({setActiveHamburger}: HeaderBottomProps) {

  const isWidthMore1023 = useMediaQuery({ query: '(max-width: 1023px)' });

  function handleActiveHamburger() {
    setActiveHamburger(prev => !prev);
  }

  return (
    <div className='menu-bottom bg-primary-900 py-6'>
      <div className='container mx-auto px-4'>
        <div className="menu-bottom__inner flex items-center justify-between xl:gap-6 lg:gap-4">
          <Logo />

          {!isWidthMore1023 && (
            <>
              <div className="flex-1">
                <SearchBlock />
              </div>
              <RegionalSettings />
              <HeaderActions />
            </>
          )}

          {isWidthMore1023 && (
            <button className={classNames('hamburger hamburger--collapse')} type="button" onClick={handleActiveHamburger}>
              <span className="hamburger-box">
                <span className="hamburger-inner"></span>
              </span>
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

export default HeaderBottom;