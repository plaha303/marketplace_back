import { clearToken, setAuthInitialized, setToken } from "../../store/slices/tokenSlice";
import store from "../../store/store";
import { axiosInstance } from "./axiosInstance";
import { ApiEndpoint } from "./enums/api-endpoint";
import { RequestOptions } from "./type/interface";
import buildRequestConfig from "./buildRequestConfig";
import axios, { AxiosResponse } from "axios";
import { getQueryClient } from "../helpers/getQueryClient";
import { normalizeApiError } from "./normalizeApiError";

export async function refreshAccessToken() {
  try {
    const response = await axiosInstance.post(ApiEndpoint.REFRESHTOKEN)
    console.log('response 1', response)
    const access_token = response.data.access;
    axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;

    console.log('access_token', access_token)

    store.dispatch(setToken(access_token));

    return access_token;
  } catch (error) {
    console.error("Error refreshing access token:", error);
    store.dispatch(clearToken());
    store.dispatch(setAuthInitialized(false));

    const queryClient = getQueryClient();
    queryClient.removeQueries({ queryKey: ['user']})

    return null;
  }
}

export async function  request<T>(options:RequestOptions): Promise<T> {
  const { method, url, body, params, config, skipAuth } = options;
  const accessToken = store.getState().token.accessToken;

  try {
    const requestConfig = buildRequestConfig({ method, accessToken: skipAuth ? undefined : accessToken, url, body, params, config });
    const response: AxiosResponse<T> = await axiosInstance(requestConfig);

    console.log('response', response)

    return response.data
  } catch (error: unknown) {
    if(axios.isAxiosError(error) && error.response?.status === 401) {
      const { isAuthInitialized } = store.getState().token;

      console.log('error isAuthInitialized', isAuthInitialized)
      if(!isAuthInitialized) {
        return Promise.reject(error)
      }

      const newAccessToken = await refreshAccessToken();
      
      if(newAccessToken) {
        const retryConfig = buildRequestConfig({ method, accessToken: newAccessToken, url, body, params, config })
        const retryResponse = await axiosInstance(retryConfig);

        return retryResponse.data
      } else {
        store.dispatch(clearToken());
         store.dispatch(setAuthInitialized(false));

        getQueryClient().removeQueries({ queryKey: ["user"]})

        return Promise.reject(new Error('Unauthorized'))
      }
    }

    const normalized = normalizeApiError(error);

    console.error("API error:", normalized);
    throw normalized;
  }
}