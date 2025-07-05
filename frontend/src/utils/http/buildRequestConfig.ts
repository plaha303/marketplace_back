import { AxiosRequestConfig } from "axios"
import { RequestOptions } from "./type/interface"

function buildRequestConfig({method, url, accessToken, body, params, config}: RequestOptions): AxiosRequestConfig {
  console.log('buildRequestConfig accessToken', accessToken)
  return {
    method,
    url,
    data: body,
    params,
    withCredentials: true,
    headers: {
      ...(config?.headers || {}),
      ...(accessToken ? { Authorization: `Bearer ${accessToken}` } : {}),
    },
    ...config
  };
}

export default buildRequestConfig;