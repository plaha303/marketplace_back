import {createSlice} from "@reduxjs/toolkit"

const initialState = {
  isOpen: false,
  modalType: null,
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
    }
  }
})

export const {openAuthModal, closeAuthModal} = authModalSlice.actions;

export default authModalSlice.reducer;