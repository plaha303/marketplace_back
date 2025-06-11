import { Link } from "react-router";
import { headerTopLinksMobile } from "./HeaderTopLinks";

function HeaderTopMobile() {
  return (
    <ul className='flex justify-center gap-6 py-1.5'>
      {headerTopLinksMobile.map(topLink => (
        <li className="menu-top__item" key={topLink.id}>
          <Link to={topLink.path} className="text-white">{topLink.icon}</Link>
        </li>
      ))}
    </ul>
  )
}

export default HeaderTopMobile;