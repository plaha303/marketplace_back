import { HttpStatusCode } from "axios";
import { ApiRequestOptions, ApiResult } from "./types";

type Constructor = {
  status?: HttpStatusCode,
  message?: string
}

export class BaseError extends Error {
  status: HttpStatusCode

  constructor({
    status = HttpStatusCode.NotAcceptable,
    message = 'Http request error'
  }: Constructor = {}) {
    super(message)

    this.name = new.target.name;
    this.status = status
  }

  static isBaseError(error: unknown) {
    if(typeof error == 'object' && error !== null && 'message' in error) {
      return true
    }

    return false
  }
}

const ERROR_NAME = 'ApiError';
export class ApiError extends BaseError {
  public readonly url: string;
  public readonly statusText: string;
  public readonly body: any;
  public readonly request: ApiRequestOptions;

  constructor(request: ApiRequestOptions, responce: ApiResult, message: string) {
    super({status: responce.status, message})

    this.name = ERROR_NAME,
    this.url = responce.url,
    this.statusText = responce.statusText,
    this.body = responce.body,
    this.request = request
  }

  static isApiError(error: unknown) {
    return BaseError.isBaseError(error) && (error as Error).name == ERROR_NAME
  }
}