import { configureStore } from "@reduxjs/toolkit";
import authModalSlice from "./authModalSlice"

const store = configureStore({
  reducer: {
    authModal: authModalSlice
  }
})

export type RootState = ReturnType<typeof store.getState>;
export default store;