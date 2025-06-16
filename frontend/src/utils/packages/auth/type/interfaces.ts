export interface LogInRequestDTO {
  email: string,
  password: string
}

export interface LogInResponseDTO { 
  email: string;
}

export interface SignUpRequestDTO {
  userName: string,
  surName: string,
  email: string,
  password: string,
  password_confirm: string,
}
export interface SignUpResponseDTO {
  success: boolean;
}