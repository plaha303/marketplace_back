import { LogInRequestDTO, LogInResponseDTO, SignUpRequestDTO, SignUpResponseDTO } from "./interfaces";

interface IAuthApi {
  logInAuth: (data: LogInRequestDTO) => Promise<LogInResponseDTO>;
  signUpAuth: (data: SignUpRequestDTO) => Promise<SignUpResponseDTO>
}

export {type IAuthApi}