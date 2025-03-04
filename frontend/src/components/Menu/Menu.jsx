import {useDispatch, useSelector} from "react-redux"
import { openAuthModal, closeAuthModal } from "../../store/authModalSlice";

import MenuBottom from "./MenuBottom";
import MenuTop from "./MenuTop";
import LogIn from "../LogIn/LogIn";
import Modal from "../../UI/Modal/Modal";
import SingUp from "../SingUp/SingUp";
import EmailConfirm from "../EmailConfirm/EmailConfirm";
import ForgotPassword from "../ForgotPassword/ForgotPassword";

function Menu() {
	const dispatch = useDispatch();
	const isModalOpen = useSelector(state => state.authModal.isOpen);
	const modalType = useSelector(state => state.authModal.modalType)

	return (
		<>
			<div className="menu-block flex flex-col grow gap-y-[24px] text-[20px]">
				<MenuTop />
				<MenuBottom />
			</div>
			{isModalOpen &&
				<Modal setIsOpenModal={isModalOpen} onClose={() => dispatch(closeAuthModal())} modalType={modalType}>
					{modalType == 'LogIn' &&  <LogIn />}
					{modalType == 'SingUp' && <SingUp />}
					{modalType == 'EmailConfirm' && <EmailConfirm />}
					{modalType == 'ForgotPassword' && <ForgotPassword />}
				</Modal>
			}
		</>
	);
}

export default Menu;