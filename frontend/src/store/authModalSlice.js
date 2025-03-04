import {createSlice} from "@reduxjs/toolkit"

const initialState = {
  isOpen: false
}

const authModalSlice = createSlice({
  name: "authModalSlice",
  initialState,
  reducers: {
    openAuthModal: (state) => {
      state.isOpen = true
    },
    closeAuthModal: (state) => [
      state.isOpen = false
    ]
  }
})

const {openAuthModal, closeAuthModal} = authModalSlice.actions;

export default authModalSlice.reducer;