import { useState } from "react";
import MenuBottom from "./MenuBottom";
import MenuTop from "./MenuTop";
import LogIn from "../LogIn/LogIn";
import Modal from "../../UI/Modal/Modal";

function Menu({toogleMenu}) {
	const [isOpenModal, setIsOpenModal] = useState(false);
	const [modalType, setModalType] = useState(null)
	console.log(modalType)
	return (
		<>
			<div className="menu-block flex flex-col grow gap-y-[24px] text-[20px]">
				<MenuTop setIsOpenModal={setIsOpenModal} setModalType={setModalType}/>
				<MenuBottom />
			</div>
			{isOpenModal &&
				<Modal setIsOpenModal={setIsOpenModal} onClose={() => setModalType(null)} modalType={modalType}>
					{modalType == 'LogIn' &&  <LogIn setIsOpenModal={setIsOpenModal} />}
				</Modal>
			}
		</>
	);
}

export default Menu;


