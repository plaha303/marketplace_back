import * as yup from "yup"
import { email, password } from "./validationFields"
import { LogInRequestDTO } from "../packages/auth/type/interfaces"

export const logInSchema: yup.ObjectSchema<LogInRequestDTO> = yup.object().shape({
  email,
  password
})