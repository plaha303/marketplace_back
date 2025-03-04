import { configureStore } from "@reduxjs/toolkit";
import authModalSlice from "./authModalSlice"

export const store = configureStore({
  reducer: {
    authModal: authModalSlice
  }
})