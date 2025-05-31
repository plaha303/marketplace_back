import { LogInRequestDTO, LogInResponseDTO, SignUpRequestDTO, SignUpResponseDTO } from "./interfaces";

interface IAuthService {
  logInAuth: (data: LogInRequestDTO) => Promise<LogInResponseDTO>;
  signUpAuth: (data: SignUpRequestDTO) => Promise<SignUpResponseDTO>
}

export {type IAuthService}