import { Outlet } from "react-router";
import Header from "../Header/Header";
import Footer from "../Footer/Footer";


import LogIn from "../../components/LogIn/LogIn";

import EmailConfirm from "../../components/EmailConfirm/EmailConfirm";
import ForgotPassword from "../../components/ForgotPassword/ForgotPassword";
import Modal from "../../UI/Modal/Modal";
import { closeAuthModal } from "../../store/authModalSlice";
import { useAppDispatch, useAppSelector } from "../../store/hooks/hooks";
import SignUp from "@/components/SignUp/SignUp";


function Layout() {
  const dispatch = useAppDispatch();
	const isModalOpen = useAppSelector(state => state.authModal.isOpen);
	const modalType = useAppSelector(state => state.authModal.modalType);

  return (
    <div className="flex flex-col min-h-screen">
      <Header />
      <main className="main flex-1">
        <div className="main__inner">
          <Outlet />
        </div>
      </main>
      {isModalOpen &&
        <Modal setIsOpenModal={isModalOpen} onClose={() => dispatch(closeAuthModal())} modalType={modalType}>
          {modalType == 'LogIn' &&  <LogIn />}
          {modalType == 'SignUp' && <SignUp />}
          {modalType == 'EmailConfirm' && <EmailConfirm />}
          {modalType == 'ForgotPassword' && <ForgotPassword />}
        </Modal>
			}
      <Footer />
    </div>
  );
}

export default Layout;