import { useAppDispatch } from "@/store/hooks/hooks";
import { clearToken, setAuthInitialized, setToken } from "@/store/slices/tokenSlice";
import { refreshAccessToken } from "@/utils/http/http-request";
import { useEffect } from "react";

export function useInitAuth() {
  const dispatch = useAppDispatch();
  let hasInitRunAuth = false;

  useEffect(() => {
    if(hasInitRunAuth) return;

    hasInitRunAuth = true;

    async function initAuth() {
      try {
        const accessToken = await refreshAccessToken();

        if(accessToken) {
          dispatch(setToken(accessToken))
        } else {
          dispatch(clearToken())
          dispatch(setAuthInitialized(false));
        }
      } catch (error) {
        console.log('initAuth error', error)
        dispatch(clearToken())
        dispatch(setAuthInitialized(false));
      } finally {
        dispatch(setAuthInitialized(true));
      }
    }

    initAuth();
  }, [])

}