import { useMediaQuery } from "react-responsive";
import HeaderTopPC from "./HeaderTopPC";
import HeaderTopMobile from "./HeaderTopMobile";

function HeaderTopLinkSection() {
  const isDesktop = useMediaQuery({ query: '(min-width: 1024px)' });

  return isDesktop ? <HeaderTopPC /> : <HeaderTopMobile />;
}

export default HeaderTopLinkSection;