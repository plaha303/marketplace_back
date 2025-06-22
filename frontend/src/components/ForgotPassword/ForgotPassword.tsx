import AuthLayout from "@/layout/AuthLayout/AuthLayout";
import AppRoute from "@/routers/enums/routers-enums";
import { Button } from "@/UI/Button/Button";
import HintIcon from "@/UI/Icons/HintIcon";
import BaseInput from "@/UI/Input/BaseInput";
import { forgotPasSchema } from "@/utils/validation/forgotPassSchema";
import { yupResolver } from "@hookform/resolvers/yup";
import { useForm } from "react-hook-form";
import { Link } from "react-router";

function ForgotPassword() {

  const {register, handleSubmit, formState: {errors}} = useForm<ForgotPassProps>({
		resolver: yupResolver(forgotPasSchema),
	});

  type ForgotPassProps = {
    email: string
  }
  function handleSubmitForgotPass(data: ForgotPassProps) {
    console.log('data', data)
  }
  return (
    <AuthLayout title="Забули пароль?">
      <div className="forgotPass__body">
        <form onSubmit={handleSubmit(handleSubmitForgotPass)} className="lg:mb-12 mb-6">
          <div className="lg:mb-12 mb-6">
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
          </div>
          <Button
						type="submit"
						className="w-full btn-primary h-14 text-size-body-2 font-bold"
					>
						Відправити підтвердження
					</Button>
        </form>

				<div className="formBottom">
					<div className="flex justify-center items-center lg:flex-row flex-col ">
						<div className="text-size-body-3 leading-130 lg:mb-0 mb-2 font-secondary">
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
    </AuthLayout>
  );
}

export default ForgotPassword;