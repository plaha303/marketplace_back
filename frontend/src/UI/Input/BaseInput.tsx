import classNames from 'classnames';
import { BaseInputProps } from './type/interface';


function BaseInput({hasError, className, ...props}: BaseInputProps) {
  return (
    <input 
      className={classNames(
        "border rounded-xl px-2.5 py-1.5 text-white w-full min-h-[55px]",
        hasError ? "border-red" : "border-white",
        className
      )}
      {...props}
    />
  );
}

export default BaseInput;