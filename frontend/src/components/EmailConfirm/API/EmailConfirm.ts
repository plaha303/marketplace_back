import { ApiEndpoint } from "@/utils/http/enums/api-endpoint"
import { HttpMethod } from "@/utils/http/enums/http-method"
import { request } from "@/utils/http/http-request"
import { EmailConfirmDTO } from "@/utils/packages/auth/type/interfaces"


export async function EmailConfirm(code: EmailConfirmDTO) {
  console.log('qwer', code)

  return request({
    url: ApiEndpoint.EMAILCONFIRM,
    method: HttpMethod.POST,
    body: code
  })
}
