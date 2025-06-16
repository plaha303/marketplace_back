import * as yup from "yup"

const regx = {
  password: /^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#&()–/[{}\]:;',?/*~$^+=<>]).+$/,
};

export const email =  yup
  .string()
  .trim()
  .required("Email обов'язкове поле")
  .email('Email повинен бути валідним')

export const password = yup.string()
  .trim()
  .required("Пароль обов'язкове поле")
   .min(8, "Пароль має містити щонайменше 8 символів")
  .test("is-valid-password", "Пароль повинен бути валідним", (value) =>
    regx.password.test(value || "")
  );

export const password_confirm = yup.string()
    .trim()
    .required("Підтвердження пароля є обов'язковим")
    .oneOf([yup.ref("password")], "Паролі не співпадають");

export const username = yup.string()
  .trim()
  .required("Ім'я обов'язкове поле");


export const surname = yup.string()
  .trim()
  .required("Прізвище обов'язкове поле")