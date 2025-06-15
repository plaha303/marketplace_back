import * as yup from "yup"

const regx = {
  password: /(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#&()–/[{}\]:;',?/*~$^+=<>])\S{8,}$/,
};

export const email =  yup
  .string()
  .trim()
  .required("Email обов'язкове поле")
  .email('Email повинен бути валідним')

export const password = yup.string()
  .trim()
  .required("Пароль обов'язкове поле")
  .test("is-valid-password", "Пароль повинен бути валідним", (value) =>
    regx.password.test(value || "")
  );