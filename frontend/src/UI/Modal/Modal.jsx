import styled from "./Modal.module.css"

function Modal({children, setIsOpenModal, modalType, onClose}) {
  function handleModalClick() {
    setIsOpenModal(false);
    onClose();
  }
  return (
    <dialog id={modalType} className="modal modal-open bg-[#fbfcf3] " onClick={handleModalClick}>
      <div className="modal-box max-w-[530px] lg:p-[40px] md:p-[20px] relative" onClick={(e) => e.stopPropagation()}>
        <span className={`${styled.closeModal}`} onClick={handleModalClick}></span>
        {children}
      </div>
    </dialog>
  );
}

export default Modal;