import { ButtonHTMLAttributes } from 'react';
import clsx from 'clsx';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {}

function Button({className, children, ...props}: ButtonProps) {
  const baseStyles = "rounded-lg text-white font-semibold custom-boxShadow"

  return (
    <button {...props} className={clsx(baseStyles, className)}>
      {children}
    </button>
  );
}

export default Button;