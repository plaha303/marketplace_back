import MenuBottom from "./MenuBottom";
import MenuTop from "./MenuTop";
import LogIn from "../LogIn/LogIn";
import Modal from "../../UI/Modal/Modal";
import SingUp from "../SingUp/SingUp";
import { useState } from "react";
import EmailConfirm from "../EmailConfirm/EmailConfirm";
import ForgotPassword from "../ForgotPassword/ForgotPassword";

function Menu() {
	const [isOpenModal, setIsOpenModal] = useState(false);
	const [modalType, setModalType] = useState(null)

	return (
		<>
			<div className="menu-block flex flex-col grow gap-y-[24px] text-[20px]">
				<MenuTop setIsOpenModal={setIsOpenModal} setModalType={setModalType} />
				<MenuBottom />
			</div>
			{isOpenModal &&
				<Modal setIsOpenModal={setIsOpenModal} onClose={() => setModalType(null)} modalType={modalType}>
					{modalType == 'LogIn' &&  <LogIn setModalType={setModalType} />}
					{modalType == 'SingUp' && <SingUp setModalType={setModalType} />}
					{modalType == 'EmailConfirm' && <EmailConfirm setModalType={setModalType} />}
					{modalType == 'ForgotPassword' && <ForgotPassword />}
				</Modal>
			}
		</>
	);
}

export default Menu;