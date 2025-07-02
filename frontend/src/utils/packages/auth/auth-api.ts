import { request } from "@/utils/http/http-request";
import { ApiEndpoint } from "@/utils/http/enums/api-endpoint";
import { HttpMethod } from "@/utils/http/enums/http-method";
import { IAuthApi } from "./type/auth-api.interface";
import { GetUserResponseDTO, LogInRequestDTO, LogInResponseDTO, SignUpRequestDTO, SignUpResponseDTO, VerifyEmailRequestDTO, VerifyEmailResponseDTO } from "./type/interfaces";

class AuthApi implements IAuthApi {
  async logInAuth(data: LogInRequestDTO): Promise<LogInResponseDTO> {
    return request({
      url: ApiEndpoint.LOGIN,
      method: HttpMethod.POST,
      body: data
    })
  };

  async signUpAuth(data: SignUpRequestDTO): Promise<SignUpResponseDTO> {
    return request({
      url: ApiEndpoint.SIGNUP,
      method: HttpMethod.POST,
      body: data
    })
  }

  async verifyEmailAuth(data: VerifyEmailRequestDTO): Promise<VerifyEmailResponseDTO> {
    const { uid, token } = data
    return request({
      url: `${ApiEndpoint.VERIFYEMAIL}/${uid}/${token}` as ApiEndpoint,
      method: HttpMethod.POST,
      body: data
    })
  }

  async getUser(): Promise<GetUserResponseDTO> {
    return request({
      url: ApiEndpoint.GETUSER,
      method: HttpMethod.GET,
    })
  }
}

export {AuthApi}