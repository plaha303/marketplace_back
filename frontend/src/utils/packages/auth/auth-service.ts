import { IAuthApi } from "./type/auth-api.interface";
import { IAuthService } from "./type/auth-service.interface";
import { LogInRequestDTO, LogInResponseDTO, SignUpRequestDTO, SignUpResponseDTO } from "./type/interfaces";


class AuthService implements IAuthService {
  private authApi: IAuthApi;

  constructor(authApi: IAuthApi) {
    this.authApi = authApi;
  } 

  async logInAuth(data: LogInRequestDTO): Promise<LogInResponseDTO> {
    return this.authApi.logInAuth(data)
  }
  
  async signUpAuth(data: SignUpRequestDTO): Promise<SignUpResponseDTO> {
    console.log('[AuthService] signUpAuth called');
    console.log('signUpAuth', data)
    return this.authApi.signUpAuth(data)
  }
}

export {AuthService}