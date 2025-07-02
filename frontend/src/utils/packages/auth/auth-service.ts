import { IAuthApi } from "./type/auth-api.interface";
import { IAuthService } from "./type/auth-service.interface";
import { GetUserResponseDTO, LogInRequestDTO, LogInResponseDTO, SignUpRequestDTO, SignUpResponseDTO, VerifyEmailRequestDTO, VerifyEmailResponseDTO } from "./type/interfaces";


class AuthService implements IAuthService {
  private authApi: IAuthApi;

  constructor(authApi: IAuthApi) {
    this.authApi = authApi;
  } 

  async logInAuth(data: LogInRequestDTO): Promise<LogInResponseDTO> {
    return this.authApi.logInAuth(data)
  }
  
  async signUpAuth(data: SignUpRequestDTO): Promise<SignUpResponseDTO> {
    return this.authApi.signUpAuth(data)
  }

  async verifyEmailAuth(data: VerifyEmailRequestDTO): Promise<VerifyEmailResponseDTO> {
    return this.authApi.verifyEmailAuth(data)
  }

  async getUser(): Promise<GetUserResponseDTO> {
    return this.authApi.getUser()
  }
}

export {AuthService}