import { AxiosRequestConfig } from "axios"
import { ApiEndpoint } from "../enums/api-endpoint"
import { HttpMethod } from "../enums/http-method"

export type RequestOptions = {
  readonly method: HttpMethod;
  readonly url: ApiEndpoint;
  readonly accessToken?: string | null,
  readonly body?: unknown;
  readonly params?: Record<string, string | number>;
  readonly config?: AxiosRequestConfig,
  readonly skipAuth?: boolean;
  readonly headers?: Record<string, string>
}

export type ApiError = {
  message: string,
  statusCode?: number;
  original?: unknown;
  fieldErrors?: Record<string, string>;
}

export type ApiResult = {
  readonly url: string,
  readonly ok: boolean
  readonly status: number,
  readonly statusText: string,
  readonly body: any,
  readonly dataErrors?: Record<string, string[]>
}

