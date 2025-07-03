import { useAppDispatch, useAppSelector } from "@/store/hooks/hooks";
import { clearToken, setAuthInitialized, setToken } from "@/store/slices/tokenSlice";
import { refreshAccessToken } from "@/utils/http/http-request";
import { useEffect, useRef } from "react";

export function useInitAuth() {
  const dispatch = useAppDispatch();
  const hasInitRunAuth = useRef<boolean>(false);

  useEffect(() => {
    if(hasInitRunAuth.current) return;

    hasInitRunAuth.current = true;

    async function initAuth() {
      try {
        const accessToken = await refreshAccessToken();

        if(accessToken) {
          dispatch(setToken(accessToken))
        } else {
          dispatch(clearToken())
        }
      } catch (error) {
        console.log('initAuth error', error)
        dispatch(clearToken())
      } finally {
        dispatch(setAuthInitialized(true));
      }
    }

    initAuth();
  }, [])

}