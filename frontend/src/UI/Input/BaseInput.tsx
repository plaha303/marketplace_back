import classNames from 'classnames';
import { BaseInputProps } from './type/interface';


function BaseInput({hasError, type, className, id, ...props}: BaseInputProps) {

  return (
    <input 
      type={type}
      autoComplete={`new-${id}`}
      className={classNames(
        `border rounded-5xl p-4 bg-snow shadow-custom1 w-full 
        hover:border-primary-100 focus:border-accent-600 disabled:bg-primary-100 
        duration-500 min-h-[55px]`,
        hasError ? "border-red-200" : "border-transparent",
        className
      )}
      {...props}
    />
  );
}

export default BaseInput;