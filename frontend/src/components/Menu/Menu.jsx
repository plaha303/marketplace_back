import MenuBottom from "./MenuBottom";
import MenuTop from "./MenuTop";
import LogIn from "../LogIn/LogIn";
import Modal from "../../UI/Modal/Modal";
import SingUp from "../SingUp/SingUp";
import { useState } from "react";

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
				</Modal>
			}
		</>
	);
}

export default Menu;