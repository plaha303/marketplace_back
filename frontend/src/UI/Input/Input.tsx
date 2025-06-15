import { FieldValues } from "react-hook-form";
import BaseInput from "./BaseInput";
import usePasswordToggle from "./hook/usePasswordToggle";
import PasswordToggle from "./PasswordToggle";
import { InputProps } from "./type/interface";

function Input<T extends FieldValues>({label, validationText, name, type, hasError, register, className}: InputProps<T>) {
  const {passwordShow, togglePassword} = usePasswordToggle();

  const isPassword = type === 'password';
  const inputType = type === 'password' && passwordShow ? 'text' : type;

  return (
    <div>
      {label && (<label className="mb-2 text-white text-xs block">{label}</label>)}
      <div className="relative">
        <BaseInput 
          className={className}
          {...register ? register(name) : {}}
          type={inputType}
          hasError={hasError}
          autoComplete={`new-${name}`}
        />
        {isPassword && (
          <PasswordToggle isVisible={passwordShow} onToggle={togglePassword} />
        )}
      </div>

      {validationText && (<div className="text-red text-xs mt-1">{validationText}</div>)}
    </div>
  );
}

export default Input;