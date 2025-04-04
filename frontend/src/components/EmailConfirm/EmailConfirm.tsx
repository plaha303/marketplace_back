import { useForm, Controller } from "react-hook-form";
import useEmailConfirmMutation from "../../hooks/Auth/useEmailConfirmMutation";
import React from "react";

function EmailConfirm() {
  const {emailConfirm, emailConfirmPending, isError, error} = useEmailConfirmMutation();

  const {control, handleSubmit, formState: { errors }, setValue, trigger, clearErrors} = useForm({
    defaultValues: {
      code: ['', '', '', '', '', ''],
    },
    mode: 'onSubmit'
  });

  async function handlePutCode(e: React.ChangeEvent<HTMLInputElement> | React.KeyboardEvent<HTMLInputElement> | React.ClipboardEvent<HTMLInputElement>, index: number) {
    if ('clipboardData' in e) {
      if (e.type === 'paste') {
        e.preventDefault();
        const pastedData = e.clipboardData.getData('text');
        const digits = pastedData.match(/\d/g);
  
        if (digits) {
          digits.forEach((digit, i) => {
            if (index + i < 6) {
              setValue(`code.${index + i}` , digit);
              clearErrors(`code.${index + i}`);
            }
          });
          const nextIndex = Math.min(index + digits.length, 5);
          const nextInput = document.getElementById(`input-${nextIndex}`);
          if (nextInput) {
            nextInput.focus();
          }
        }
        return;
      }
    }
    
    if ('key' in e && e.key === 'Backspace') {
      if (e.key === 'Backspace') {
        if ((e.target as HTMLInputElement).value === '') {
          if (index > 0) {
            setValue(`code.${index - 1}` as const, '');
            clearErrors(`code.${index - 1}` as const);
            const prevInput = document.getElementById(`input-${index - 1}`);
            if (prevInput) {
              prevInput.focus();
            }
          }
        } else {
          setValue(`code.${index}`, '');
          clearErrors(`code.${index}`);
        }
        return;
      }
    }

    
    if ('target' in e) {
      const value = (e.target as HTMLInputElement).value;
      if (value === '' || (value.length === 1 && /^[0-9]$/.test(value))) {
        setValue(`code.${index}`, value);
        clearErrors(`code.${index}`);

        if (value.length === 1 && index < 5) {
          const nextInput = document.getElementById(`input-${index + 1}`);
          if (nextInput) {
            nextInput.focus();
          }
        }
      }
    }

    await trigger();
  }


  type EmailConfirmProps = {
    code: string[]
  }
  function onSubmitPassword(data: EmailConfirmProps) {
    console.log(data)
    const code = data.code.join('');
    console.log('Submitted code:', code);

    emailConfirm({code})
  }

  // const handleChange = async (e: React.ChangeEvent<HTMLInputElement>, index: number) => {
  //   handlePutCode(e, index);
  //   await trigger();
  // }

  return (
    <>
      <div className="modal-header mb-[36px]">
				<h2 className="text-2xl font-semibold mb-2 pe-[40px]">Введіть код підтвердження</h2>
				<div className="modalSubtitle font-medium text-base">
          Для завершення процесу входу введіть шестизначний код підтвердження, надісланий на вашу електронну пошту.
				</div>
			</div>

      <div className="modal-body">
        <form onSubmit={handleSubmit(onSubmitPassword)}>
          <div className="md:p-[40px] p-[20px]">
            <div className="font-medium lg:leading-[1.5] leading lg:text-2xl text-[19px] text-center lg:mb-[40px] mb-[20px]">
              Введіть код підтвердження
            </div>
            <div className="flex justify-center lg:mb-[40px] mb-[20px]">
              <div className="flex justify-center gap-x-[20px]  max-w-[245px]">
                {[...Array(6)].map((_, index) => (
                  <div className="inputCode w-[24px] h-[40px]" key={index}>
                    <Controller
                      name={`code.${index}` as const}
                      control={control}
                      rules={{
                        required: 'Этот код обязательный',
                        validate: {
                          // length: (value) => value.length === 6 || 'Код должен содержать 6 цифр',
                          validate: (value) => value.length === 1 || 'Каждое поле должно быть заполнено цифрой',
                        },
                        pattern: {
                          value: /^[0-9]$/,
                          message: 'Код должен содержать только цифры',
                        },
                      }}
                      render={({ field }) => (
                        <input
                          {...field}
                          type="text"
                          maxLength={1}
                          id={`input-${index}`}
                          onChange={(e) => {
                            handlePutCode(e, index);
                            field.onChange(e);
                          }}
                          onKeyDown={(e) => handlePutCode(e, index)}
                          onPaste={(e) => handlePutCode(e, index)}
                          className="bg-[#f9fafb] border border-[#01060b] rounded-xs w-full h-full text-center font-medium"
                        />
                      )}
                    />
                  </div>
                ))}
              </div>
              {errors.code && (
              <div className="text-red-500">
                {errors.code[0]?.message || 'Пожалуйста, введите корректный код'}
              </div>
            )}
            </div>
            <div>
              {isError && error && <div className="error-message">{error.message || 'An unknown error occurred'}</div>}
            </div>
            <div className="lg:w-[240px] w-full mx-auto">
              <button type="submit" disabled={emailConfirmPending} className="w-full rounded-lg text-white font-semibold text-2xl p-2 leading-[1.5] formBtn">Відправити</button>
            </div>
          </div>
        </form>
      </div>
    </>
  );
}

export default EmailConfirm;