import { request } from "@/utils/http/http-request";
import { ApiEndpoint } from "@/utils/http/enums/api-endpoint";
import { HttpMethod } from "@/utils/http/enums/http-method";
import { IAuthApi } from "./type/auth-api.interface";
import { LogInRequestDTO, LogInResponseDTO, SignUpRequestDTO, SignUpResponseDTO } from "./type/interfaces";

class AuthApi implements IAuthApi {
  async logInAuth(data: LogInRequestDTO): Promise<LogInResponseDTO> {
    return request({
      url: ApiEndpoint.LOGIN,
      method: HttpMethod.POST,
      body: data
    })
  };

  async signUpAuth(data: SignUpRequestDTO): Promise<SignUpResponseDTO> {
    console.log('api', data)
    return request({
      url: ApiEndpoint.SIGNUP,
      method: HttpMethod.POST,
      body: data
    })
  }
}

export {AuthApi}