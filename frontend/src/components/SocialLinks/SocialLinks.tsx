import { Link } from 'react-router';
import { socialLinks, SocialLinksProps } from './interfaces';
import classNames from 'classnames';

function SocialLinks({className, colorIcon="text-snow"}: SocialLinksProps) {
  return (
    <ul className={classNames('flex justify-center gap-6 py-1.5', className)}>
      {socialLinks.map(link => {
        const Icon = link.icon;
        return (
          <li className="menu-top__item" key={link.id}>
            <Link to={link.path} className={colorIcon}>
              <Icon />
            </Link>
          </li>
        )
      })}
    </ul>
  );
}

export default SocialLinks;