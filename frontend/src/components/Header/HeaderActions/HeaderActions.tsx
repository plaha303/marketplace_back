import AppRoute from "@/routers/enums/routers-enums";
import BasketIcon from "@/UI/Icons/BasketIcon";
import FavoriteIcon from "@/UI/Icons/FavoriteIcon";
import NotificationIcon from "@/UI/Icons/NotificationIcon";
import UserIcon from "@/UI/Icons/UserIcon";
import { Link } from "react-router";

import styled from "./HeaderActions.module.scss"
import classNames from "classnames";
import SearchIcon from "@/UI/Icons/SearchIcon";
import { useAppSelector } from "@/store/hooks/hooks";
import { Button } from "@/UI/Button/Button";

function HeaderActions({handleOpenUserMenu}: {handleOpenUserMenu: () => void;}) {
  const isAccessToken = useAppSelector(state => state.token.accessToken);
  const isAuthInitialized = useAppSelector(state => state.token.isAuthInitialized);

  console.log('isAuthInitialized', isAuthInitialized)
  console.log('header isAccessToken', isAccessToken)

  return (
    <div className="menuActions flex lg:flex-row flex-col  lg:items-center lg:gap-4">
      <div className={`${styled.menuAction} lg:order-3 order-3`}>
        <Link to={AppRoute.NOTIFICATION} className="flex items-center">
          <div className="relative">
            <NotificationIcon className="text-snow hover:text-accent-600 duration-500" />
            <span className={classNames('bg-red-100', styled.menuAction__notificationDot)}></span>
          </div>
          <span className="lg:hidden text-size-body-3 ml-2 text-snow block font-bold">Сповіщення</span>
        </Link>
      </div>

      <div className={`${styled.menuAction} lg:hidden block order-2`}>
        <Link to={AppRoute.FAVORITE} className="flex items-center">
          <SearchIcon className="text-snow hover:text-accent-600 duration-500" />
          <span className="text-size-body-3 ml-2 text-snow hover:text-accent-600 duration-500 font-bold">Пошук</span>
        </Link>
      </div>

      <div className={`${styled.menuAction} lg:order-2 order-4`}>
        <Link to={AppRoute.FAVORITE} className="flex items-center">
          <FavoriteIcon className="text-snow hover:text-accent-600 duration-500" />
          <span className="lg:hidden text-size-body-3 ml-2 text-snow font-bold">Обране</span>
        </Link>
      </div>
      <div className={`${styled.menuAction} lg:order-3 order-5`}>
        <Link to={AppRoute.BASKET} className="flex items-center">
          <div className="relative">
            <BasketIcon className="text-snow hover:text-accent-600 duration-500" />
            <span className={classNames('bg-red-100', styled.menuAction__basketCount)}>2</span>
          </div>
          <span className="lg:hidden text-size-body-3 ml-2 text-snow font-bold">Корзина</span>
        </Link>
      </div>
      <div className={`${styled.menuAction} lg:order-4 order-0`}>
        {!isAccessToken 
          ? (
            <Link to={AppRoute.LOGIN} className="flex items-center">
              <UserIcon className="text-snow hover:text-accent-600 duration-500" />
              <span className="lg:hidden text-size-body-3 ml-2 text-snow block font-bold">Вхід</span>
            </Link>
          ) : (
            <Button type="button" className="p-0 bg-transparent w-auto h-auto" onClick={() => handleOpenUserMenu()}>
              <span className="flex items-center justify-center lg:w-[56px] lg:h-[56px] h-[40px] w-[40px] bg-primary-100 hover:bg-primary-100 p-0 rounded-full">
                <UserIcon className="text-primary-900 hover:text-accent-600" />
              </span>
              <span className="lg:hidden text-size-body-3 ml-2 text-snow block font-bold">Профіль</span>
            </Button>
          )
        }
      </div>
      
    </div>
  );
}

export default HeaderActions;