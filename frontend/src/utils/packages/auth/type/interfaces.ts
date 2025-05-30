export interface LogInRequestDTO {
  email: string,
  password: string
}

export interface LogInResponseDTO { 
  email: string;
}

export interface SignUpRequestDTO {
  userName: string,
  email: string,
  password: string,
  password2: string,
}
export interface SignUpResponseDTO {
  success: boolean;
}