import PlatformsButtons from "../platformsButtons/platformsButtons";
import styled from "../../UI/Modal/Modal.module.css"
import { useForm } from "react-hook-form";

function LogIn({setModalType}) {
  const {handleSubmit, register, formState: {errors}, watch} = useForm();
  function onSubmit(data) {
    console.log(data)
  }

  return (
		<>
			<div className="modal-header mb-[36px]">
				<h2 className="text-2xl font-semibold mb-2 pe-[40px]">Увійти</h2>
				<div className="modalSubtitle font-medium text-base">
					Ласкаво просимо до [Назва Вебсайту]! Введіть свої дані, щоб отримати
					доступ до вашого акаунту.
				</div>
			</div>

			<div className="modal-body">
				<form autoComplete="false" onSubmit={handleSubmit(onSubmit)}>
					<div className="mb-4">
						<div className="mb-2">Email</div>
						<input
              {...register("email", {required: true})}
							name="email"
							type="email"
							autoComplete="off"
							placeholder="ivan.kosak@gmail.com"
							className={`block w-full rounded-lg bg-white 
                placeholder:text-gray-400 input h-[37px] ps-4 pe-4 pt-2 pb-2 
                focus:border-grey-600 duration-500 border-[#616163] border
                shadow-[0_2px_4px_0_rgba(0,0,0,0.15);]
                ${errors.email ? '!input-error' : '' }
              `}
						/>
            {errors.email &&
              <div className="flex items-center text-red-600 font-medium mt-2">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="h-6 w-6 shrink-0 stroke-current"
                  fill="none"
                  viewBox="0 0 24 24">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
                This field is required
              </div>
            }
					</div>
					<div className="mb-[36px]">
						<div className="mb-2 flex justify-between">
							<div>Пароль</div>
							<button
								type="button"
								className="hover:text-blue-600 duration-500"
							>
								Забули пароль?
							</button>
						</div>
						<input
              {...register("password", {required: true})}
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
            {errors.password &&
              <div className="flex items-center text-red-600 font-medium mt-2">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="h-6 w-6 shrink-0 stroke-current"
                  fill="none"
                  viewBox="0 0 24 24">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
                This field is required
              </div>
            }
					</div>

					<button
						type="submit"
						className="w-full rounded-lg text-white font-semibold text-2xl p-2 leading-[1.5] formBtn"
					>
						Увійти
					</button>

          <div className={`${styled.separateBlock} relative text-center lg:mt-[32px] lg:mb-[24px] md:mb-[20px] md:mt-[20px]`}>
            <span className="bg-white relative z-10 ps-[22px] pe-[22px] separateBlock__text leading-[2] inline-block">увійти за допомогю</span>
          </div>

          <PlatformsButtons />
				</form>

        <div className="formBottom text-base mt-3 pt-2 border-t-[#01060b] border-t">
          <div className="flex justify-between items-center md:flex-col lg:flex-row">
            <div className="lg:max-w-[210px] md:max-w-full lg:mb-0 md:mb-4">
              Ще не маєте облікового запису?
            </div>
            <button type="button" className="font-medium btn bg-transparent border-0 shadow-none lg:w-[210px] md:w-full" onClick={() => setModalType('SingUp')}>Зареєструватися</button>
          </div>
        </div>
			</div>
		</>
	);
}

export default LogIn;