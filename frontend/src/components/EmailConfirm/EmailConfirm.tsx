import { useForm, Controller } from "react-hook-form";
import useEmailConfirmMutation from "./hook/useEmailConfirmMutation";
import AuthLayout from "@/layout/AuthLayout/AuthLayout";
import { InputOTP, InputOTPGroup, InputOTPSlot } from "@/UI/InputOTP/InputOTP";
import { REGEXP_ONLY_DIGITS_AND_CHARS } from "input-otp"
import { useLocation, useNavigate } from "react-router";
import { useEffect, useState } from "react";
import { CustomError, EmailConfirmDTO } from "@/utils/packages/auth/type/interfaces";
import { Button } from "@/UI/Button/Button";
import { yupResolver } from "@hookform/resolvers/yup";
import { emailConfirmSchema } from "@/utils/validation/emailConfirmSchema";
import AppRoute from "@/routers/enums/routers-enums";
import HintIcon from "@/UI/Icons/HintIcon";

function EmailConfirm() {
  const location = useLocation();
  const navigate = useNavigate();

  const email = location.state?.email;

   useEffect(() => {
    if (!email) {
      navigate('/register');
    }
  }, [email]);

  const {emailConfirm, emailConfirmPending, isError, error} = useEmailConfirmMutation();

  const {control, handleSubmit, formState: { errors }, setError} = useForm<EmailConfirmDTO>({
    defaultValues: {
      verification_code: '',
    },
    resolver: yupResolver(emailConfirmSchema),
  });


  const [globalError, setGlobalError] = useState('');

  function onSubmitPassword(data: EmailConfirmDTO) {
    console.log('Submitted code:', data);

    emailConfirm(data, {
      onSuccess: () => {
				navigate('/');
			},
      onError: (error: Error) => {
        console.log('error', error)
        const customError = error as CustomError;
        let hasFieldErrors = false;

        if(customError.original) {
          Object.entries(customError.original).forEach(([field, message]) => {
            const errorMessage = Array.isArray(message) ? message[0] : message;
            setError(field as keyof EmailConfirmDTO, {
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
    <AuthLayout title="Введіть код підтвердження" subtitle="Для завершення процесу входу введіть шестизначний код підтвердження, надісланий на вашу електронну пошту.">
      <div className="modal-body">
        <form onSubmit={handleSubmit(onSubmitPassword)}>
          <div className="md:p-[40px] p-[20px]">
            <div className="font-medium lg:leading-[1.5] leading lg:text-2xl text-[19px] text-center lg:mb-[40px] mb-[20px]">
              Введіть код підтвердження
            </div>
            <div className="mb-4">
              <div className="flex justify-center">
                <Controller 
                  control={control}
                  name="verification_code"
                  render={({ field }) => (
                    <InputOTP maxLength={6} pattern={REGEXP_ONLY_DIGITS_AND_CHARS} {...field}>
                      <InputOTPGroup>
                        <InputOTPSlot index={0} />
                        <InputOTPSlot index={1} />
                        <InputOTPSlot index={2} />
                        <InputOTPSlot index={3} />
                        <InputOTPSlot index={4} />
                        <InputOTPSlot index={5} />
                      </InputOTPGroup>
                    </InputOTP>
                  )}
                />
              </div>

              {errors?.verification_code && (
                <div className="flex items-center text-red-600 font-medium mb-2">
                  <HintIcon className="text-red-200 flex items-center mr-1" />
                  <span className="text-red-600 text-size-body-4 leading-130 font-secondary">{errors.verification_code.message}</span>
                </div>
              )}
            </div>

            {globalError && (
              <p style={{ color: "red" }} className="mb-4">
                {globalError}
              </p>
            )}
            

            <div className="">
              <Button type="submit" disabled={emailConfirmPending} className="w-full font-bold leading-100 text-size-body-2 btn-primary h-14">
                Відправити
              </Button>
            </div>
          </div>
        </form>
      </div>
    </AuthLayout>
  );
}

export default EmailConfirm;