import React, { PropsWithChildren } from 'react';
import styled from "./Modal.module.scss"
import { closeAuthModal } from "../../store/authModalSlice";
import { useRef } from "react";
import { useAppDispatch } from '../../store/hooks/hooks';

interface ModalProps {
  modalType: string | null,
  setIsOpenModal: boolean,
  onClose: () => void
}

const Modal: React.FC<PropsWithChildren<ModalProps>> = ({ children, modalType }) => {
  const dispatch = useAppDispatch()
  const dialogRef = useRef<HTMLDialogElement | null>(null);

  function handleModalClick(e: React.MouseEvent<HTMLSpanElement>) {
    if(e.target === e.currentTarget) {
      dispatch(closeAuthModal())
      // dialogRef.current?.close();
    }
    
  }
  return (
    <dialog ref={dialogRef}  id={modalType || ''} className="modal modal-open bg-[#fbfcf3] " onMouseDown={(e) => handleModalClick(e)}>
      <div className="modal-box max-w-[530px] lg:p-[40px] md:p-[20px] relative" onClick={(e) => e.stopPropagation()}>
        <span className={`${styled.closeModal}`} onMouseDown={(e) => handleModalClick(e)}></span>
        {children}
      </div>
    </dialog>
  );
}

export default Modal;