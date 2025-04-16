import { configureStore } from "@reduxjs/toolkit";
import authModalSlice from "./authModalSlice"
import { saveCodeSentToLocalStorage } from "./middleware/middleware";

const store = configureStore({
  reducer: {
    authModal: authModalSlice
  },
  middleware: 
    (getDefaultMiddleware) => getDefaultMiddleware().concat(saveCodeSentToLocalStorage)

})

export type RootState = ReturnType<typeof store.getState>;
export default store;