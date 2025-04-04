import { useForm } from "react-hook-form";

function ForgotPassword() {

  const {register, handleSubmit, formState: {errors}} = useForm<ForgotPassProps>();


  type ForgotPassProps = {
    email: string
  }
  function handleSubmitForgotPass(data: ForgotPassProps) {
    console.log('data', data)
  }
  return (
    <>
     <div className="modal-header mb-[36px]">
				<h2 className="text-2xl font-semibold mb-2 pe-[40px]">Забули пароль?</h2>
				<div className="modalSubtitle font-medium text-base">
          Ви забули свій пароль? Не хвилюйтеся, це трапляється з кожним! 
          Для відновлення доступу до Вашого облікового запису введіть Вашу пошту.
				</div>
			</div> 

      <div className="modal-body">
        <form onSubmit={handleSubmit(handleSubmitForgotPass)}>
          <div className="mb-[32px]">
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
          </div>
          <button
						type="submit"
						className="w-full rounded-lg text-white font-semibold text-2xl p-2 leading-[1.5] formBtn"
					>
						Відправити
					</button>
        </form>
      </div>
    </>
  );
}

export default ForgotPassword;