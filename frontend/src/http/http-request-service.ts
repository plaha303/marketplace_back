import axios, { AxiosError, AxiosRequestConfig, AxiosResponse } from "axios"
import { isBlob, isDefined, isFormData, isString, isSuccess, shallowStringify } from "../helpers/helpers";
import { ApiRequestOptions, ApiResult } from "./types";
import { ApiError } from "./api-error";

axios.defaults.baseURL = import.meta.env.VITE_BASE_URL;
axios.defaults.headers.common['Content-Type'] = 'application/x-www-form-urlencoded'

function catchErrorCode(options: ApiRequestOptions, result: ApiResult) {
  const errors: Record<number, string> = {
    400: 'Bad Request',
    401: 'Unauthorized',
    403: 'Forbidden',
    404: 'Not Found',
    422: 'Unprocessable entity',
    500: 'Internal Server Error',
    502: 'Bad Gateway',
    503: 'Service Unavailable',
    800: 'Network Timeout',
    ...options.errors,
  };

  const message: string = errors[result.status] ?? 'Unknown error';

  if (result.dataErrors && Object.keys(result.dataErrors).length > 0) {
    const dataErrors = new ApiError(options, result, message);
    (dataErrors as any).errors = result.dataErrors;
    throw dataErrors;
  }

  if(message) {
    throw new ApiError(options, result, message)
  }

  if (!result.ok) {
    throw new ApiError(options, result, 'Generic Error');
  }
  
}

function getResponseHeader(response: AxiosResponse<any>, responseHeader?: string) {
  if(responseHeader) {
    const content = response.headers[responseHeader];
    if(isString(content)) {
      return content
    }
  }

  return undefined
}

function getResponseBody(response: AxiosResponse<any>) {
  if(response.status !== 204) {
    return response.status
  }

  return undefined
}

function getQueryString(params: Record<string, any>): string {
  const qs: string[] = [];

  const append = (key: string, value: any) => {
    qs.push(`${encodeURIComponent(key)}=${encodeURIComponent(String(value))}`)
  }

  const progress = (key: string, value: any) => {
    if(isDefined(value)) {
      if(Array.isArray(value)) {
        value.forEach(val => {
          progress(key, val)
        })
      } else if(typeof value == 'object') {
        Object.entries(value).forEach(([k, v]) => {
          progress(`${key} [${k}]`, v)
        })
      } else {
        append(key, value)
      }
    }
  }

  Object.entries(params).forEach(([key, value]) => {
    progress(key, value)
  })

  if(qs.length > 0) {
    return `?${qs.join('&')}`
  }
  
  return ''
}

function getUrl(options: ApiRequestOptions): string {
  const path = options.url.replace(/{(.*?)}/g, 
    (substring: string, group: string) => {
      if(options.path?.hasOwnProperty(group)) {
        return encodeURI(String(options.path[group]))
      }

      return substring;
    }
  )

  if(options.query) {
    return `${path}${getQueryString(options.query)}`
  }

  return path;
}

const getFormData = (options: ApiRequestOptions): FormData | undefined => {
  if (options.formData) {
    const formData = new FormData();

    const process = (key: string, value: any) => {
      if (isString(value) || isBlob(value)) {
        formData.append(key, value);
      } else {
        formData.append(key, JSON.stringify(value));
      }
    };

    Object.entries(options.formData)
      .filter(([_, value]) => isDefined(value))
      .forEach(([key, value]) => {
        if (Array.isArray(value)) {
          value.forEach((v) => process(key, v));
        } else {
          process(key, value);
        }
      });

    return formData;
  }
  return undefined;
};

async function getHeaders(options: ApiRequestOptions, formData?: FormData) {
  const headers = Object.entries({Accept: 'application/json', ...options.headers})
                  .filter(([_, value]) => isDefined(value))
                  .reduce(
                    (_headers, [key, value]) => ({
                      ..._headers,
                      [key]: String(value),
                    }),
                    {} as Record<string, string>,
                  );
    
  if(options.body) {
    if(options.mediaType) {
      headers['Content-type'] = options.mediaType
    } else if(isBlob(options.body)) {
      headers['Content-type'] = options.body.type || 'application/octet-stream';
    } else if(isString(options.body)) {
      headers['Content-type'] = 'text/plain'
    } else if(!isFormData(options.body)) {
      headers['Content-type'] = 'application/json'
    }
  }

  return headers;
}

async function sendRequest<T>(url: string,options: ApiRequestOptions, body: any, formData: FormData | undefined, headers: Record<string, string> ): Promise<AxiosResponse<T>> {
  const source = axios.CancelToken.source();

  const requestConfig: AxiosRequestConfig = {
    url,
    headers,
    data: body ?? formData,
    method: options.method,
    cancelToken: source.token
  }

  console.log("Axios Base URL:", axios.defaults.baseURL);
  console.log("Final Request URL:", requestConfig.url);

  try {
    if(import.meta.env.DEV) {
      console.debug(
        `${requestConfig.method}] HTTP Request: `,
        shallowStringify({
          baseUrl: axios.defaults.baseURL,
          endpoint: requestConfig.url,
          body: requestConfig.data,
          headers: requestConfig.headers,
        })
      )
    }
  
    return await axios.request(requestConfig);
  } catch (error) {
    const axiosError = error as AxiosError<T>;

    if (axiosError.response) {
      return axiosError.response;
    }
    throw error;
  }
}

export function Request<T>(options: ApiRequestOptions): Promise<T> {
  return new Promise((res, rej) => {
    (async() => {
      console.log('options', options)

      try {
        const url = getUrl(options);

        const formData = getFormData(options);
        const body = options.body;
        const headers = await getHeaders(options, formData)

        const response = await sendRequest<T>(
          url,
          options,
          body,
          formData,
          headers
        )

        const responseBody = getResponseBody(response);
        const responseHeader = getResponseHeader(response, options.responseHeader);

        const result: ApiResult = {
          url,
          ok: isSuccess(response.status),
          status: response.status,
          statusText: response.statusText,
          body: responseHeader ?? responseBody,
          dataErrors: (response.data as any)?.errors
        }

        catchErrorCode(options, result)

        res(result.body)
      } catch (error) {
        if (error instanceof ApiError) {
          console.error(`[${options.method}] - ${error.status} error:`, {
            details: error.body,
            url: error.url,
          });
        } else if (error instanceof AxiosError) {
          console.error(`[${options.method}]Axios error:`, {
            message: error.message,
            baseUrl: error.config?.baseURL ?? '',
            url: error.config?.url ?? '',
          });
        } else {
          console.error(`[${options.method}] Unknown error:`, {
            error,
          });
        }
        rej(error);
      }
    })();
  })
}