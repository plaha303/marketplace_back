import * as yup from "yup"
import { password, password_confirm } from "./validationFields";

export const changePassSchema = yup.object().shape({
  password,
  password_confirm
})