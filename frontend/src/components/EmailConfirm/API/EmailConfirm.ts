import { ApiEndpoint } from "@/utils/http/enums/api-endpoint"
import { HttpMethod } from "@/utils/http/enums/http-method"
import { request } from "@/utils/http/http-request"


export interface EmailConfirmProps {
  code: string
}

export async function EmailConfirm(code: EmailConfirmProps) {
  console.log('qwer', code)

  return request({
    url: ApiEndpoint.EMAILCONFIRM,
    method: HttpMethod.POST,
    body: code
  })
}
