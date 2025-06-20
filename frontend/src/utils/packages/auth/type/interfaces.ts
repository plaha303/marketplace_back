export interface LogInRequestDTO {
  email: string,
  password: string
}

export interface LogInResponseDTO { 
  email: string;
}

export interface SignUpRequestDTO {
  username: string,
  surname: string,
  email: string,
  password: string,
  password_confirm: string,
}
export interface SignUpResponseDTO {
  success: boolean;
}

export interface CustomError {
  original?: Record<string, string>,
  message: string,
  fieldErrors?: Record<string, string>
}

export interface EmailConfirmDTO {
  verification_code: string
}