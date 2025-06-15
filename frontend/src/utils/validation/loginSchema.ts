import * as yup from "yup"
import { email, password } from "./validationFields"

export const logInSchema = yup.object().shape({
  email,
  password
})