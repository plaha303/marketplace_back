import { GetUserResponseDTO, LogInRequestDTO, LogInResponseDTO, SignUpRequestDTO, SignUpResponseDTO, VerifyEmailRequestDTO, VerifyEmailResponseDTO } from "./interfaces";

interface IAuthService {
  logInAuth: (data: LogInRequestDTO) => Promise<LogInResponseDTO>;
  signUpAuth: (data: SignUpRequestDTO) => Promise<SignUpResponseDTO>;
  verifyEmailAuth: (data: VerifyEmailRequestDTO) => Promise<VerifyEmailResponseDTO>;
  getUser: () => Promise<GetUserResponseDTO>;
  logOutAuth: () => void;
}

export {type IAuthService}