import { Link } from 'react-router';
import { ButtonLinkProps } from './type/interface';
import classNames from 'classnames';

function ButtonLink({children, className, to, ...props}: ButtonLinkProps) {
  return (
    <Link to={to} {...props} className={classNames('btn', className)}>
      {children}
    </Link>
  );
}

export default ButtonLink;