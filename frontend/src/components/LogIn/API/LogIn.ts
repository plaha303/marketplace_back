import { ApiEndpoint } from "@/utils/http/enums/api-endpoint"
import { HttpMethod } from "@/utils/http/enums/http-method"
import { request } from "@/utils/http/http-request"


export interface LogInProps {
  email: string,
  password: string
}

export async function LogIn(data: LogInProps) {
  return request({
    url: ApiEndpoint.LOGIN,
    method: HttpMethod.POST,
    body: data
  })
}
