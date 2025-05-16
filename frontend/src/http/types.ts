import { ContentType } from "./enums/content-type"
import { type HttpMethod } from "./enums/http-method"

export type ApiRequestOptions = {
  readonly method: HttpMethod,
  readonly url: string,
  readonly path?: Record<string, any>,
  readonly cookies?: Record<string, any>,
  readonly headers?: Record<string, any>,
  readonly query?: Record<string, any>,
  readonly formData?: Record<string, any>,
  readonly body?: any,
  readonly mediaType?: ContentType,
  readonly responseHeader?:  any,
  readonly errors?: Record<number, string>
}

export type ApiResult = {
  readonly url: string,
  readonly ok: boolean
  readonly status: number,
  readonly statusText: string,
  readonly body: any,
  readonly dataErrors?: Record<string, string[]>
}