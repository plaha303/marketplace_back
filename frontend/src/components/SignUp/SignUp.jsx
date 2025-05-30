import { useForm } from "react-hook-form"

import styled from "@/UI/Modal/Modal.module.scss"

import { openAuthModal } from "../../store/authModalSlice";
import PlatformsButtons from "../PlatformsButtons/PlatformsButtons";
import { useAppDispatch } from "../../store/hooks/hooks";
import useSignUpMutation from "./hook/useSignUpMutation";


function SignUp() {
  const dispatch = useAppDispatch();
	const {mutateSignUp, mutateSignUpPenging, isError, error} = useSignUpMutation();
  const {handleSubmit, register, formState: {errors}, watch, setError} = useForm();

  function onSubmit(data) {
		mutateSignUp(data, {
			onError: (error) => {
				console.log('asd', error)
				const fieldErrors = error.fieldErrors;

				if(fieldErrors) {
					Object.entries(fieldErrors).forEach(([field, message]) => {
						setError(field, {type: "server", message})
					})
				}
			}
		});
  }


  return (
		<>
			<div className="modal-header mb-[36px]">
				<h2 className="text-2xl font-semibold mb-2 pe-[40px]">
					Зареєструватися
				</h2>
				<div className="modalSubtitle font-medium text-base">
					Ласкаво просимо до [Назва Вебсайту]! Введіть свої дані, щоб отримати
					доступ до вашого акаунту.
				</div>
			</div>

			<div className="modal-body">
				<form autoComplete="off" onSubmit={handleSubmit(onSubmit)}>
					<div className="mb-[32px]">
						<div className="mb-4">
							<div className="mb-2">Ім’я та прізвище</div>
							<input
								{...register('username', {
									required: "Це поле обов'язкове для заповнення",
									validate: {
										notEmpty: (value) =>
											value.trim() !== '' || 'Ім’я та прізвище не може бути пустим',
									},
								})}
								name="username"
								type="text"
								autoComplete="username"
								placeholder="Іван  Козак"
								className={`block w-full rounded-lg bg-white 
                placeholder:text-gray-400 input h-[37px] ps-4 pe-4 pt-2 pb-2 
                focus:border-grey-600 duration-500 border-[#616163] border
                shadow-[0_2px_4px_0_rgba(0,0,0,0.15);]
                ${errors.username ? '!input-error' : ''}`}
							/>
							{errors?.username && (
								<div className="flex items-center text-red-600 font-medium mt-2">
									<svg
										xmlns="http://www.w3.org/2000/svg"
										className="h-6 w-6 shrink-0 stroke-current"
										fill="none"
										viewBox="0 0 24 24"
									>
										<path
											strokeLinecap="round"
											strokeLinejoin="round"
											strokeWidth="2"
											d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
										/>
									</svg>
									{errors.username.message}
								</div>
							)}
						</div>
						<div className="mb-4">
							<div className="mb-2">Email</div>
							<input
								{...register('email', {
									required: "Це поле обов'язкове для заповнення",
									validate: {
										notEmpty: (value) =>
											value.trim() !== '' || 'Пошта не може бути пустою',
										validEmail: (value) =>
											/\S+@\S+\.\S+/.test(value) ||
											'Будь-ласка, введіть коректну пошту',
									},
								})}
								name="email"
								type="email"
								autoComplete="email"
								placeholder="ivan.kosak@gmail.com"
								className={`block w-full rounded-lg bg-white 
                  placeholder:text-gray-400 input h-[37px] ps-4 pe-4 pt-2 pb-2 
                  focus:border-grey-600 duration-500 border-[#616163] border
                  shadow-[0_2px_4px_0_rgba(0,0,0,0.15);]
                  ${errors.email ? '!input-error' : ''}
                `}
							/>
							{errors.email && (
								<div className="flex items-center text-red-600 font-medium mt-2">
									<svg
										xmlns="http://www.w3.org/2000/svg"
										className="h-6 w-6 shrink-0 stroke-current"
										fill="none"
										viewBox="0 0 24 24"
									>
										<path
											strokeLinecap="round"
											strokeLinejoin="round"
											strokeWidth="2"
											d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
										/>
									</svg>
									{errors.email.message}
								</div>
							)}
						</div>
						<div className="mb-4">
							<div className="mb-2 flex justify-between">
								<div>Пароль</div>
							</div>
							<input
								{...register('password', {
									required: "Це поле обов'язкове для заповнення",
									minLength: {
										value: 8,
										message: 'Пароль повинен містити не менше 8 символів',
									},
									validate: {
										notEmpty: (value) =>
											value.trim() !== '' || 'Пароль не може бути пустим',
										hasUppercase: (value) =>
											/[A-Z]/.test(value) ||
											'Пароль повинен містити хоча б одну велику літеру',
										hasLowercase: (value) =>
											/[a-z]/.test(value) ||
											'Пароль повинен містити хоча б одну малу літеру',
										hasDigit: (value) =>
											/[0-9]/.test(value) ||
											'Пароль повинен містити хоча б одну цифру',
									},
								})}
								name="password"
								type="password"
								autoComplete="off"
								placeholder="Ввести пароль"
								className={`block w-full rounded-lg bg-white 
                  placeholder:text-gray-400 input h-[37px] ps-4 pe-4 pt-2 pb-2 
                  focus:border-grey-600 duration-500 border-[#616163] border
                  shadow-[0_2px_4px_0_rgba(0,0,0,0.15);]
                  ${errors.password ? '!input-error' : ''}
                `}
							/>
							{errors.password && (
								<div className="flex items-center text-red-600 font-medium mt-2">
									<svg
										xmlns="http://www.w3.org/2000/svg"
										className="h-6 w-6 shrink-0 stroke-current"
										fill="none"
										viewBox="0 0 24 24"
									>
										<path
											strokeLinecap="round"
											strokeLinejoin="round"
											strokeWidth="2"
											d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
										/>
									</svg>
									{errors.password.message}
								</div>
							)}
						</div>
						<div className="mb-4">
							<div className="mb-2 flex justify-between">
								<div>Підтвердити пароль</div>
							</div>
							<input
								{...register('password2', {
									required: "Це поле обов'язкове для заповнення",
									minLength: {
										value: 8,
										message: 'Пароль повинен містити не менше 8 символів',
									},
									validate: {
										notMatch: (value) =>
											value === watch('password') || 'Паролі не співпадають',
										notEmpty: (value) =>
											value.trim() !== '' || 'Пароль не може бути пустим',
										hasUppercase: (value) =>
											/[A-Z]/.test(value) ||
											'Пароль повинен містити хоча б одну велику літеру',
										hasLowercase: (value) =>
											/[a-z]/.test(value) ||
											'Пароль повинен містити хоча б одну малу літеру',
										hasDigit: (value) =>
											/[0-9]/.test(value) ||
											'Пароль повинен містити хоча б одну цифру',
									},
								})}
								name="password2"
								type="password"
								autoComplete="off"
								placeholder="Ввести пароль"
								className={`block w-full rounded-lg bg-white 
                  placeholder:text-gray-400 input h-[37px] ps-4 pe-4 pt-2 pb-2 
                  focus:border-grey-600 duration-500 border-[#616163] border
                  shadow-[0_2px_4px_0_rgba(0,0,0,0.15);]
                  ${errors.password2 ? '!input-error' : ''}
                `}
							/>
							{errors.password2 && (
								<div className="flex items-center text-red-600 font-medium mt-2">
									<svg
										xmlns="http://www.w3.org/2000/svg"
										className="h-6 w-6 shrink-0 stroke-current"
										fill="none"
										viewBox="0 0 24 24"
									>
										<path
											strokeLinecap="round"
											strokeLinejoin="round"
											strokeWidth="2"
											d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
										/>
									</svg>
									{errors.password2.message}
								</div>
							)}
						</div>
						<div className="error-block text-red-600"></div>
					</div>

					{isError && (!error?.fieldErrors || Object.keys(error.fieldErrors).length === 0) && (
						<p style={{ color: "red", marginBottom: '15px' }}>{error.message}</p>
					)}

					<button
						type="submit"
						className="w-full rounded-lg text-white font-semibold text-2xl p-2 leading-[1.5] btn-blue"
					>
						Зареєструватися
					</button>

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
								onClick={() => dispatch(openAuthModal('LogIn'))}
							>
								Увійти
							</button>
						</div>
					</div>
				</form>
			</div>
		</>
	);
}

export default SignUp;