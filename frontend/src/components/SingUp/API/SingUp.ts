import { ApiEndpoint } from "@/utils/http/enums/api-endpoint"
import { HttpMethod } from "@/utils/http/enums/http-method"
import { request } from "@/utils/http/http-request"


export interface SingUpProps {
  userName: string,
  email: string,
  password: string,
  password2: string,
}


export async function SingUp(data: SingUpProps) {
  console.log('SingUp', data)
  
  return request({
    url: ApiEndpoint.SINGUP,
    method: HttpMethod.POST,
    body: data
  })
}