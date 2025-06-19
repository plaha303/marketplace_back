import * as yup from "yup"
import { email } from "./validationFields";

export const forgotPasSchema = yup.object().shape({
  email
})