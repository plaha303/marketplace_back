import {createSlice} from "@reduxjs/toolkit"

const getInitialIsCodeSent = (): boolean => {
  if(typeof window !== 'undefined') {
    const stored = localStorage.getItem('isCodeSent');

    return stored ? JSON.parse(stored) : false
  }

  return false;
}

const initialState = {
  isOpen: false,
  modalType: null,
  isCodeSent: getInitialIsCodeSent()
}

const authModalSlice = createSlice({
  name: "authModalSlice",
  initialState,
  reducers: {
    openAuthModal: (state, action) => {
      state.isOpen = true
      state.modalType = action.payload
    },
    closeAuthModal: (state) => {
      state.isOpen = false,
      state.modalType = null
    },
    setCodeSent: (state, action) => {
      state.isCodeSent = action.payload
    }
  }
})

export const {openAuthModal, closeAuthModal, setCodeSent} = authModalSlice.actions;

export default authModalSlice.reducer;