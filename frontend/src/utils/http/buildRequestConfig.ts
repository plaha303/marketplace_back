import { AxiosRequestConfig } from "axios"
import { RequestOptions } from "./type/interface"

function buildRequestConfig({method, url, body, params, config, headers}: RequestOptions): AxiosRequestConfig {
  return {
    method,
    url,
    data: body,
    params,
    withCredentials: true,
    headers: {
      ...(config?.headers || {}),
      ...(headers || {}),
    },
    ...config
  };
}

export default buildRequestConfig;