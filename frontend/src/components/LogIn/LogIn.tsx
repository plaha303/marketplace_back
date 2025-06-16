import PlatformsButtons from "../PlatformsButtons/PlatformsButtons";
import { useForm } from "react-hook-form";
import useLogInMutation from "./hook/useLogInMutation";
import { yupResolver } from "@hookform/resolvers/yup"

import styled from "./Login.module.scss"
import { useState } from "react";

import BaseInput from "@/UI/Input/BaseInput";
import PasswordToggle from "@/UI/Input/PasswordToggle";
import usePasswordToggle from "@/UI/Input/hook/usePasswordToggle";
import { Link } from "react-router";
import AppRoute from "@/routers/enums/routers-enums";
import { Button } from "@/UI/Button/Button";
import { logInSchema } from "@/utils/validation/loginSchema";
import HintIcon from "@/UI/Icons/HintIcon";
import classNames from "classnames";
import { CustomError, LogInRequestDTO } from "@/utils/packages/auth/type/interfaces";

function LogIn() {
	const [globalError, setGlobalError] = useState('');

	const {passwordShow, togglePassword} = usePasswordToggle();
	const {mutateLogIn, mutateLoginPending} = useLogInMutation();
  const {handleSubmit, register, formState: {errors}, setError} = useForm<LogInRequestDTO>({
    resolver: yupResolver(logInSchema),
  });


  function onSubmit(data: LogInRequestDTO) {
		mutateLogIn(data, {
			onError: (error: Error) => {
				console.log('error', error)
				const customError = error as CustomError;
				let hasFieldErrors = false;

				if(customError.original) {
					Object.entries(customError.original).forEach(([field, message]) => {
						const errorMessage = Array.isArray(message) ? message[0] : message;
						setError(field as keyof LogInRequestDTO, {
							type: 'server',
							message: errorMessage,
						});
						hasFieldErrors = true;
					});
				}

				if(!hasFieldErrors && customError.message) {
					setGlobalError(customError.message);
				}
			}
		})
  }

  return (

			<div className="login__block max-w-[685px] mx-auto bg-snow-70 shadow-custom1 lg:p-12 px-6 py-10 rounded-5xl">
				<div className="login__header lg:mb-12 mb-6">
					<h2 className="login__title text-size-h2 mb-2 leading-100 text-accent-800">Увійти</h2>
					<div className="login__subtitle text-size-body-1 leading-130">
						Вітаємо на нашому маркетплейсі! 
					</div>
				</div>

				<div className="login-body">
					<form autoComplete="false" onSubmit={handleSubmit(onSubmit)} className="lg:mb-12 mb-6">
						<div className="lg:mb-12 mb-6">
							<div className="mb-4">
							<label className="block mb-1 font-size-body-4 leading-130">Електронна адреса <sup className="text-red-200 font-size-body-4">*</sup></label>
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
										<span className="text-red-600 text-size-body-4 leading-130">{errors.email.message}</span>
									</div>
								)}
							</div>
							<div className="mb-4">
								<div className="flex justify-end">
									<Link to={AppRoute.RESET_PASSWORD} className="text-size-link-1 text-primary-600 leading-100 hover:underline duration-500">Забули пароль?</Link>
								</div>
								<div className="mb-2">
									<label className="block mb-1 font-size-body-4 leading-130">Пароль <sup className="text-red-200 font-size-body-4">*</sup></label>
								</div>
								<div className="relative">
									<BaseInput
										id="password"
										{...register('password')}
										className="rounded-5xl font-secondary pr-12"
										placeholder="Введіть пароль"
										type={passwordShow ? "text" : "password"}
										hasError={!!errors.password}
									/>
									<PasswordToggle onToggle={togglePassword} isVisible={passwordShow} 
										iconClassName={classNames('text-primary-400', !!errors.password ? 'text-red-200' : '')} 
									/>
								</div>
								{errors.password && (
									<div className="flex items-center text-red-600 text-size-body-4 leading-130 mt-1">
										<HintIcon className="text-red-200 flex items-center mr-1"/>
										{errors.password.message}
									</div>
								)}
							</div>
						</div>


						{globalError && (
							<p style={{ color: "red" }} className="mb-4">
								{globalError}
							</p>
						)}

						<Button
							type="submit"
							className="w-full font-bold leading-100 text-size-body-2 btn-primary h-14"
							size="md"
							disabled={mutateLoginPending}
						>
							Увійти
						</Button>
					</form>

					<div className={`${styled.separateBlock} relative text-center mb-6`}>
						<span className="bg-transparent relative z-10 px-2 text-primary-400 separateBlock__text leading-130 inline-block">
							або увійти з
						</span>
					</div>

						<PlatformsButtons />
					

					<div className="formBottom">
						<div className="flex justify-center items-center lg:flex-row flex-col ">
							<div className="text-size-body-3 leading-130 lg:mb-0 mb-2">
								Ще не зареєстровані?
							</div>
							<Link to={AppRoute.REGISTRATION}
								className="text-primary-600 text-size-link-1 ml-2 leading-100"
							>
								Реєстрація
							</Link>
						</div>
					</div>

				</div>
			</div>
	);
}

export default LogIn;