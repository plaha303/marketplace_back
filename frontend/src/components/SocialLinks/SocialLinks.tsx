import { Link } from 'react-router';
import { socialLinks } from './interfaces';
import classNames from 'classnames';

function SocialLinks({className}: {className?: string}) {
  return (
    <ul className={classNames('flex justify-center gap-6 py-1.5', className)}>
      {socialLinks.map(link => (
        <li className="menu-top__item" key={link.id}>
          <Link to={link.path} className="text-white">{link.icon}</Link>
        </li>
      ))}
    </ul>
  );
}

export default SocialLinks;