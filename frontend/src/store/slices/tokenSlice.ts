import { createSlice } from "@reduxjs/toolkit";

export interface TokenDTO {
  accessToken: string | null;
  isAuthInitialized: boolean;
}

const initialState: TokenDTO = {
  accessToken: null,
  isAuthInitialized: false,
}

export const tokenSlice = createSlice({
  name: 'token', 
  initialState,
  reducers: {
    setToken: (state, action) => {
      state.accessToken = action.payload
    },
    clearToken: (state) => {
      state.accessToken = null;
      state.isAuthInitialized = false;
    },
    setAuthInitialized: (state) => {
      state.isAuthInitialized = true;
    }
  }
})

export const {setToken, clearToken, setAuthInitialized} = tokenSlice.actions;

export default tokenSlice.reducer;