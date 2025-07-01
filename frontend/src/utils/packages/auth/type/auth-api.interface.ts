import { LogInRequestDTO, LogInResponseDTO, SignUpRequestDTO, SignUpResponseDTO, VerifyEmailRequestDTO, VerifyEmailResponseDTO } from "./interfaces";

interface IAuthApi {
  logInAuth: (data: LogInRequestDTO) => Promise<LogInResponseDTO>;
  signUpAuth: (data: SignUpRequestDTO) => Promise<SignUpResponseDTO>;
  verifyEmailAuth: (data: VerifyEmailRequestDTO) => Promise<VerifyEmailResponseDTO>;
}

export {type IAuthApi}