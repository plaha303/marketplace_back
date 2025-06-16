import AuthLayout from "@/layout/AuthLayout/AuthLayout";
import { Button } from "@/UI/Button/Button";
import ErrorCheckIcon from "@/UI/Icons/ErrorCheckIcon";
import HintIcon from "@/UI/Icons/HintIcon";
import SuccessCheckIcon from "@/UI/Icons/SuccessCheckIcon";
import BaseInput from "@/UI/Input/BaseInput";
import PasswordToggle from "@/UI/Input/PasswordToggle";
import { changePassSchema } from "@/utils/validation/changePassSchema";
import { yupResolver } from "@hookform/resolvers/yup";
import classNames from "classnames";
import { useState } from "react";
import { useForm } from "react-hook-form";

function ChangePassword() {
  const [showPassword, setShowPassword] = useState(false);
  const [showPasswordConfirm, setShowPasswordConfirm] = useState(false);
  const togglePasswordConfirm = () => setShowPasswordConfirm((prev) => !prev);

  const {register, handleSubmit, watch, formState: {errors}} = useForm({
    resolver: yupResolver(changePassSchema),
  });

  const togglePassword = () => setShowPassword((prev) => !prev);

  const passwordValue = watch('password');
	const isLengthValid = passwordValue ? passwordValue.length >= 8 : '';
	const hasUpperCase = /[A-Z]/.test(passwordValue);
	const hasNumber = /\d/.test(passwordValue);
	const hasSpecialChar = /[!@#&()–/[{}\]:;',?/*~$^+=<>]/.test(passwordValue);

  function onSubmit(data) {
    console.log('data', data)
  }

  return (
    <AuthLayout title="Введіть новий пароль">
      <form className="" onSubmit={handleSubmit(onSubmit)}>
        <div className="lg:mb-12 mb-6">
          <div className="mb-4">
            <label className="block mb-1 font-size-body-4 leading-130 font-secondary">Пароль <sup className="text-red-200 font-size-body-4">*</sup></label>
            <div className="relative">
              <BaseInput 
                {...register('password')}
                type={showPassword ? "text" : "password"}
                autoComplete="password"
                placeholder="Ввести пароль"
                hasError={!!errors.password}
                className="rounded-5xl font-secondary"
              />
              <PasswordToggle onToggle={togglePassword} isVisible={showPassword} 
                iconClassName={classNames('text-primary-400', !!errors.password ? 'text-red-200' : '')} 
              />
            </div>
            
            {errors.password && (
              <div className="flex items-center text-red-600 font-medium mt-2">
                <HintIcon className="text-red-200 flex items-center mr-1" />
                <span className="text-red-600 text-size-body-4 leading-130 font-secondary">{errors.password.message}</span>
              </div>
            )}

            {passwordValue && (<div>
              <div className="text-size-body-4 font-secondary text-primary-500 mb-2">Ваш пароль має:</div>
                <ul className='list-none'>
                  <li className="flex items-center mb-2">
                    {hasUpperCase ? <SuccessCheckIcon className="text-green-200" /> : <ErrorCheckIcon className="text-red-200" /> }
                    <span className="text-primary-500 text-size-body-4 font-secondary ml-1">Включати великі та малі літери</span>
                  </li>
                  <li className="flex items-center mb-2">
                    {hasNumber ? <SuccessCheckIcon className="text-green-200" /> : <ErrorCheckIcon className="text-red-200" /> }
                    <span className="text-primary-500 text-size-body-4 font-secondary ml-1">Включати цифри</span>
                  </li>
                  <li className="flex items-center mb-2">
                    {isLengthValid ? <SuccessCheckIcon className="text-green-200" /> : <ErrorCheckIcon className="text-red-200" /> }
                    <span className="text-primary-500 text-size-body-4 font-secondary ml-1">Бути не менш ніж 8 символів</span>
                  </li>
                  <li className="flex items-center mb-2">
                    {hasSpecialChar ? <SuccessCheckIcon className="text-green-200" /> : <ErrorCheckIcon className="text-red-200" /> }
                    <span className="text-primary-500 text-size-body-4 font-secondary ml-1">Принаймні один спеціальний символ.</span>
                  </li>
                </ul>
              </div>
            )}
          </div>
          <div className="mb-4">
            <label className="block mb-1 font-size-body-4 leading-130 font-secondary">Підтвердити пароль <sup className="text-red-200 font-size-body-4">*</sup></label>
            <div className="relative">
              <BaseInput 
                {...register('password_confirm')}
                type={showPasswordConfirm ? "text" : "password"}
                autoComplete="password_confirm"
                placeholder="Підтвердити пароль"
                hasError={!!errors.password_confirm}
                className="rounded-5xl font-secondary"
              />
              <PasswordToggle onToggle={togglePasswordConfirm} isVisible={showPasswordConfirm} 
                iconClassName={classNames('text-primary-400', !!errors.password_confirm ? 'text-red-200' : '')} 
              />
            </div>
            {errors.password_confirm && (
              <div className="flex items-center text-red-600 font-medium mt-2">
                <HintIcon className="text-red-200 flex items-center mr-1" />
                <span className="text-red-600 text-size-body-4 leading-130 font-secondary">{errors.password_confirm.message}</span>
              </div>
            )}
          </div>
        </div>

        <Button
          type="submit"
          size="md"
          className="w-full  btn-primary h-[55px] font-secondary text-size-body-2 font-bold leading-100"
        >
          Зберегти
        </Button>
      </form>
    </AuthLayout>
  );
}

export default ChangePassword;