import { Request } from "../../http/http-request-service";
import { HttpMethod } from "../../http/enums/http-method";
import { ApiEndpoint } from "../../http/enums/api-endpoint";

export interface EmailConfirmProps {
  code: string
}

export async function EmailConfirm(code: EmailConfirmProps) {
  console.log('qwer', code)

  return Request({
    url: ApiEndpoint.EMAILCONFIRM,
    method: HttpMethod.POST,
    body: code
  })
}
