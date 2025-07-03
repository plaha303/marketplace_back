import { userMenuLinks, userMenuLinksSettings } from "./type/interface";
import SingOut from '@/assets/Icons/SignOut.svg?react';
import UserIcon from '@/assets/Icons/User.svg?react'
import useGetUserQuery from "@/hooks/auth/useGetUserQuery";
import { Link } from "react-router";

function UserMenu({handleCloseUserMenu}: {handleCloseUserMenu: () => void}) {
  const {getUserProfile} = useGetUserQuery();
  
  return (
    <div className="user-menu h-full bg-snow rounded-tl-sm py-6 px-4 rounded-bl-sm shadow-custom1  overflow-y-auto">
      <div className="user-menu__inner">

        <div className="user-menu__top mb-6 flex items-center">
          <div className="user-menu__avatar rounded-full w-[56px] h-[56px] mr-4">
            <span className="flex items-center justify-center lg:w-[56px] lg:h-[56px] h-[40px] w-[40px] bg-primary-100 p-0 rounded-full">
              <UserIcon className="text-primary-900" />
            </span>
          </div>
          <div className="user-menu__top-right">
            <div className="user-menu__name text-size-h7 font-bold leading-130 mb-2">{getUserProfile?.surname} {getUserProfile?.surname}</div>
            <div className="user-menu__contact text-size-h7 text-primary-600 leading-130">{getUserProfile?.email}</div>
          </div>
        </div>

        <div className="user-menu__items">
          {userMenuLinks.map(item => {
            const LinkIcon = item.icon;
            return (
              <div className="user-menu__item mb-2" key={item.id}>
                <Link to={item.path} onClick={() => handleCloseUserMenu()} className="flex items-center text-size-body-3 font-bold p-4 font-secondary">
                  <span className="mr-2"><LinkIcon /></span>
                  {item.title}
                </Link>
              </div>
            )            
          })}
        </div>

        <div className="user-menu__items mt-2 border-t border-t-primary-100">
          {userMenuLinksSettings.map(item => {
            const LinkIcon = item.icon;
            return (
              <div className="user-menu__item mb-2" key={item.id}>
                <Link to={item.path} onClick={() => handleCloseUserMenu()} className="flex items-center text-size-body-3 font-bold p-4 font-secondary">
                  <span className="mr-2"><LinkIcon /></span>
                  {item.title}
                </Link>
              </div>
            )
          })}
        </div>

        <div className="user-menu__items mt-2 border-t border-t-primary-100">
          <div className="user-menu__item flex items-center text-size-body-3 font-bold p-4 font-secondary">
            <span className="mr-2"><SingOut /></span>
            Вийти
          </div>
        </div>

      </div>
    </div>
  );
}

export default UserMenu;