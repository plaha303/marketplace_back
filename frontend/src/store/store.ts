import { configureStore } from "@reduxjs/toolkit";
import authModalSlice from "./authModalSlice"
import { saveCodeSentToLocalStorage } from "./middleware/middleware";
import tokenReducer from "./slices/tokenSlice";

const store = configureStore({
  reducer: {
    authModal: authModalSlice,
    token: tokenReducer,
  },
  middleware: 
    (getDefaultMiddleware) => getDefaultMiddleware().concat(saveCodeSentToLocalStorage)

})

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
export default store;