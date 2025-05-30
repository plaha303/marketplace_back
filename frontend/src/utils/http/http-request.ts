import { useQueryClient } from "@tanstack/react-query";
import { clearToken, setToken } from "../../store/slices/tokenSlice";
import store from "../../store/store";
import { axiosInstance } from "./axiosInstance";
import { ApiEndpoint } from "./enums/api-endpoint";
import { RequestOptions } from "./type/interface";
import buildRequestConfig from "./buildRequestConfig";
import axios, { AxiosResponse } from "axios";
import { getQueryClient } from "../../helpers/getQueryClient";
import { normalizeApiError } from "./normalizeApiError";

export async function refreshAccessToken() {
  try {
    const responce = await axiosInstance.post(ApiEndpoint.REFRESHTOKEN)
    
    const access_token = responce.data.data.access_token;

    store.dispatch(setToken(access_token));

  } catch (error) {
    console.error("Error refreshing access token:", error);

    const queryClient = useQueryClient();
    queryClient.removeQueries({ queryKey: ['user']})

    return null;
  }
}

export async function  request<T>(options:RequestOptions): Promise<T> {
  const { method, url, body, params, config } = options;
  const accessToken = store.getState().token.accessToken;

  try {
    const requestConfig = buildRequestConfig({ method, accessToken, url, body, params, config });
    const response: AxiosResponse<T> = await axiosInstance(requestConfig);

    console.log('response', response)

    return response.data
  } catch (error: unknown) {
    if(axios.isAxiosError(error) && error.response?.status === 401) {
      const {isAuthInitialized} = store.getState().token;

      if(!isAuthInitialized) {
        return Promise.reject(error)
      }

      const newAccessToken = await refreshAccessToken();
      
      if(newAccessToken) {
        const retryConfig = buildRequestConfig({ method, accessToken: newAccessToken, url, body, params, config })
        const retryResponce = await axiosInstance(retryConfig);

        return retryResponce.data
      } else {
        store.dispatch(clearToken());

        getQueryClient().removeQueries({ queryKey: ["user"]})

        return Promise.reject(new Error('Unauthorized'))
      }
    }

    const normalized = normalizeApiError(error);

    console.error("API error:", normalized);
    throw normalized;
  }
}