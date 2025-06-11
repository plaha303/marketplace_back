import { headerTopLinks } from './HeaderTopLinks';
import { Link } from 'react-router';

function HeaderTopPC() {
  return (
    <ul className='flex lg:flex-row flex-col lg:items-center justify-center lg:gap-x-14 gap-y-3'>
      {headerTopLinks.map(topLink => (
        <li className="menu-top__item" key={topLink.id}>
          <Link to={topLink.path} className="link-1 lg:text-white text-primary-900 py-1 px-2 block">{topLink.label}</Link>
        </li>
      ))}
    </ul>
  )
}

export default HeaderTopPC;