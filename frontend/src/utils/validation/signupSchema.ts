import * as yup from "yup"
import { email, password, password_confirm, surname, username } from "./validationFields"
import { SignUpRequestDTO } from "../packages/auth/type/interfaces"

export const signupSchema: yup.ObjectSchema<SignUpRequestDTO> = yup.object().shape({
  username,
  surname,
  email,
  password,
  password_confirm
})