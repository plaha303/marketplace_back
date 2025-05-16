import { Middleware } from "@reduxjs/toolkit";
import { setCodeSent } from "../authModalSlice";

export const saveCodeSentToLocalStorage: Middleware = store => next => (action: any) => {
  const result = next(action);

  if(action.type === setCodeSent.type) {
    const isCodeSent = store.getState().authModal.isCodeSent;

    localStorage.setItem('isCodeSent', JSON.stringify(isCodeSent))
  }

  return result;
}

