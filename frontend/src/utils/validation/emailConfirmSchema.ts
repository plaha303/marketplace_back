import { EmailConfirmDTO } from "../packages/auth/type/interfaces";
import * as yup from "yup"
import { verification_code } from "./validationFields";

export const emailConfirmSchema: yup.ObjectSchema<EmailConfirmDTO> = yup.object().shape({
  verification_code
})