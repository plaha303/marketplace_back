import { Outlet } from "react-router";

import Header from "../Header/Header";
import Footer from "../Footer/Footer";

import LogIn from "../../components/LogIn/LogIn";
import SingUp from "../../components/SingUp/SingUp";
import EmailConfirm from "../../components/EmailConfirm/EmailConfirm";
import ForgotPassword from "../../components/ForgotPassword/ForgotPassword";
import Modal from "../../UI/Modal/Modal";
import { closeAuthModal } from "../../store/authModalSlice";
import { useAppDispatch, useAppSelector } from "../../store/hooks/hooks";

function Layout() {
  const dispatch = useAppDispatch();
	const isModalOpen = useAppSelector(state => state.authModal.isOpen);
	const modalType = useAppSelector(state => state.authModal.modalType);

  return (
    <>
      <Header />
        <main className="main">
          <div className="container mx-auto">
            <Outlet />
          </div>
        </main>
        {isModalOpen &&
				<Modal setIsOpenModal={isModalOpen} onClose={() => dispatch(closeAuthModal())} modalType={modalType}>
					{modalType == 'LogIn' &&  <LogIn />}
					{modalType == 'SingUp' && <SingUp />}
					{modalType == 'EmailConfirm' && <EmailConfirm />}
					{modalType == 'ForgotPassword' && <ForgotPassword />}
				</Modal>
			}
      <Footer />
    </>
  );
}

export default Layout;