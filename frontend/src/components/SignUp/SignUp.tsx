import { useForm } from "react-hook-form"

import styled from "@/UI/Modal/Modal.module.scss"

import PlatformsButtons from "../PlatformsButtons/PlatformsButtons";
import useSignUpMutation from "./hook/useSignUpMutation";
import BaseInput from "@/UI/Input/BaseInput";
import HintIcon from "@/UI/Icons/HintIcon";
import { yupResolver } from "@hookform/resolvers/yup";
import { signupSchema } from "@/utils/validation/signupSchema";
import PasswordToggle from "@/UI/Input/PasswordToggle";
import classNames from "classnames";
import { useState } from "react";
import SuccessCheckIcon from "@/UI/Icons/SuccessCheckIcon";
import ErrorCheckIcon from "@/UI/Icons/ErrorCheckIcon";
import { Checkbox } from "@/UI/Checkbox/checkbox";
import { Button } from "@/UI/Button/Button";

interface onSubmitProps {
	username: string;
	surname: string;
	email: string;
	password: string;
	password_confirm: string;
}


function SignUp() {
	const [showPassword, setShowPassword] = useState(false);
	const [showPasswordConfirm, setShowPasswordConfirm] = useState(false);
	const [agreeTerms, setAgreeTerms] = useState(false);
	const togglePassword = () => setShowPassword((prev) => !prev);
	const togglePasswordConfirm = () => setShowPasswordConfirm((prev) => !prev);


	const {mutateSignUp, mutateSignUpPenging, isError, error} = useSignUpMutation();
  const {handleSubmit, register, formState: {errors}, watch, setError} = useForm<onSubmitProps>({
		resolver: yupResolver(signupSchema),
	});

  function onSubmit(data: onSubmitProps) {
		mutateSignUp(data, {
			onError: (error) => {
				const fieldErrors = error.fieldErrors;

				if(fieldErrors) {
					Object.entries(fieldErrors).forEach(([field, message]) => {
						setError(field, {type: "server", message})
					})
				}
			}
		});
  }

	function handleAgreeTerms() {
		setAgreeTerms(prev => !prev)
	}

	const passwordValue = watch('password');
	const isLengthValid = passwordValue ? passwordValue.length >= 8 : '';
	const hasUpperCase = /[A-Z]/.test(passwordValue);
	const hasNumber = /\d/.test(passwordValue);
	const hasSpecialChar = /[!@#&()–/[{}\]:;',?/*~$^+=<>]/.test(passwordValue);

  return (
		<div className="signup__block max-w-[685px] mx-auto bg-snow-70 shadow-custom1 lg:p-12 px-6 py-10 rounded-5xl">
			<div className="login__header lg:mb-12 mb-6">
				<h2 className="login__title text-size-h2 mb-2 leading-100 text-accent-800">Реєстрація у системі</h2>
				<div className="login__subtitle text-size-body-1 leading-130">
					Вітаємо на нашому маркетплейсі! 
				</div>
			</div>

			<div className="signup-body">
				<form autoComplete="off" onSubmit={handleSubmit(onSubmit)}>
					<div className="lg:mb-12 mb-6">
						<div className="flex lg:gap-6 lg:flex-row flex-col">
							<div className="mb-4 flex-1/2">
								<label className="block mb-1 font-size-body-4 leading-130 font-secondary">Ім’я <sup className="text-red-200 font-size-body-4">*</sup></label>
								<BaseInput 
									{...register('username')}
									type="text"
									autoComplete="username"
									placeholder="Ім’я"
									hasError={!!errors.email}
									className="rounded-5xl font-secondary"
								/>
								{errors?.username && (
									<div className="flex items-center text-red-600 font-medium mt-2">
										<HintIcon className="text-red-200 flex items-center mr-1" />
										<span className="text-red-600 text-size-body-4 leading-130 font-secondary">{errors.username.message}</span>
									</div>
								)}
							</div>
							<div className="mb-4 flex-1/2">
								<label className="block mb-1 font-size-body-4 leading-130">Прізвище <sup className="text-red-200 font-size-body-4">*</sup></label>
								<BaseInput 
									{...register('surname')}
									type="text"
									autoComplete="surname"
									placeholder="Прізвище"
									hasError={!!errors.surname}
									className="rounded-5xl font-secondary"
								/>
								{errors.surname && (
									<div className="flex items-center text-red-600 font-medium mt-2">
										<HintIcon className="text-red-200 flex items-center mr-1" />
										<span className="text-red-600 text-size-body-4 leading-130 font-secondary">{errors.surname.message}</span>
									</div>
								)}
							</div>
						</div>

						<div className="mb-4">
							<label className="block mb-1 font-size-body-4 leading-130 font-secondary">Електронна адреса <sup className="text-red-200 font-size-body-4">*</sup></label>
								<BaseInput 
									id="email"
									type="text"
									inputMode="email"
									hasError={!!errors.email}
									{...register('email')}
									placeholder="Email"
									className="rounded-5xl font-secondary"
								/>
								{errors.email && (
									<div className="flex items-center  mt-1">
										<HintIcon className="text-red-200 flex items-center mr-1"/>
										<span className="text-red-600 text-size-body-4 leading-130 font-secondary">{errors.email.message}</span>
									</div>
								)}
							</div>

						<div className="flex lg:gap-6 lg:flex-row flex-col">
							<div className="flex-1/2">
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
								</div>
							</div>
							<div className="flex-1/2">
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
						</div>

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


						<div className="mt-4">
							<label className="flex items-center">
								<Checkbox className="w-5 h-5" checked={agreeTerms} onCheckedChange={(checked) => setAgreeTerms(checked === true)} />
								<span className="ml-3 font-secondary text-size-body-5 text-primary-600">Погоджуюсь з умовами та політикою конфіденційності</span>
							</label>
						</div>
					</div>

					{isError && (!error?.fieldErrors || Object.keys(error.fieldErrors).length === 0) && (
						<p style={{ color: "red", marginBottom: '15px' }}>{error.message}</p>
					)}

					

					<Button
						disabled={!agreeTerms ? true : false}
						type="submit"
						size="md"
						className="w-full  btn-primary h-[55px] font-secondary text-size-body-2 font-bold leading-100"
					>
						Зареєструватися
					</Button>

					<div
						className={`${styled.separateBlock} relative text-center lg:mt-[32px] lg:mb-[24px] md:mb-[20px] md:mt-[20px]`}
					>
						<span className="bg-white relative z-10 ps-[22px] pe-[22px] separateBlock__text leading-[2] inline-block">
							зареєструватися за допомогю
						</span>
					</div>

					<PlatformsButtons />

					<div className="formBottom text-base mt-3 pt-2 border-t-[#01060b] border-t">
						<div className="flex justify-between items-center md:flex-col lg:flex-row">
							<div className="lg:max-w-[240px] md:max-w-full lg:mb-0 md:mb-4">
								Вже маєте обліковий запис?
							</div>
							<button
								type="button"
								className="font-medium btn bg-transparent border-0 shadow-none lg:w-[120px] md:w-full"
							>
								Увійти
							</button>
						</div>
					</div>
				</form>
			</div>
		</div>
	);
}

export default SignUp;