import * as yup from "yup"
import { email, password, password_confirm, surname, username } from "./validationFields"

export const signupSchema = yup.object().shape({
  username,
  surname,
  email,
  password,
  password_confirm
})