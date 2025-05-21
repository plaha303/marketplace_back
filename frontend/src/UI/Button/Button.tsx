import classNames from 'classnames';
import { ButtonProps } from './type/interface';

function Button({children, className, ...props}: ButtonProps) {
  return (
    <button className={classNames('btn', className)} {...props}>
      {children}
    </button>
  );
}

export default Button;