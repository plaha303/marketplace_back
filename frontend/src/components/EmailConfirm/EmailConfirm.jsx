import { useState } from "react";
import { useForm } from "react-hook-form";

function EmailConfirm({setModalType}) {

  const [codeValue, setCodeValue] = useState(["", "", "", "", "", ""]);

  function handlePutCode(e, index) {
    const newCodeValue = [...codeValue]
    const value = e.target.value;

    if(value === "" || (value.length === 1 && /^[0-9]$/.test(value))) {
      newCodeValue[index] = value
      setCodeValue(newCodeValue)
    }

    if(value.length === 1 && index <  codeValue.length-1) {
      const nextInput = document.getElementById(`input-${index + 1}`);
      if (nextInput) {
        nextInput.focus();
      }
    }    
  }

  const {handleSubmit} = useForm();

  function onSubmitPassword(data) {
    console.log(data)
  }



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
              Введіть шестизначний код підтвердження
            </div>
            <div className="flex justify-center lg:mb-[40px] mb-[20px]">
              <div className="flex justify-center gap-x-[20px]  max-w-[245px]">
                {codeValue.map((codeNumber, index) => (
                  <div className="inputCode w-[24px] h-[40px]" key={index}>
										<input
											type="text"
											id={`input-${index}`} 
                      value={codeNumber}
                      maxLength={1}
                      onChange={(e) => handlePutCode(e, index)}
											className="bg-[#f9fafb] border border-[#01060b] rounded-xs w-full h-full text-center [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none font-medium"
										/>
									</div>
                ))}
              </div>
            </div>
            <div className="lg:w-[240px] w-full mx-auto">
              <button type="button" className="w-full rounded-lg text-white font-semibold text-2xl p-2 leading-[1.5] formBtn">Відправити</button>
            </div>
          </div>
        </form>
      </div>
    </>
  );
}

export default EmailConfirm;