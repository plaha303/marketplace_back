import { ApiEndpoint } from "../../http/enums/api-endpoint"
import { HttpMethod } from "../../http/enums/http-method"
import { Request } from "../../http/http-request-service"

export interface SingUpProps {
  userName: string,
  email: string,
  password: string,
  password2: string,
}


export async function SingUp(data: SingUpProps) {
  console.log('SingUp', data)
  
  return Request({
    url: ApiEndpoint.SINGUP,
    method: HttpMethod.POST,
    body: data
  })
}