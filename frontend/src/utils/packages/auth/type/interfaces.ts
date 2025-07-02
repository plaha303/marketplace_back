export interface LogInRequestDTO {
  email: string,
  password: string
}

export interface LogInResponseDTO { 
  email: string;
  access: string;
  success: boolean
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

export interface VerifyEmailRequestDTO {
  uid: string; 
  token: string
}

export interface VerifyEmailResponseDTO {
  success: boolean,
  message: string
}

export interface GetUserResponseDTO {
  data: {
    username: string;
    surname: string;
    email: string;
    roles: string[];
  },
  success: boolean
}