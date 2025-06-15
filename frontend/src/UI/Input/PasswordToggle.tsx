import CloseEyeIcon from "../Icons/CloseEyeIcon";
import OpenEyeIcon from "../Icons/OpenEyeIcon";
import { PasswordToggleProps } from "./type/interface";

const PasswordToggle = ({onToggle, isVisible, iconClassName}: PasswordToggleProps) => {
  return (
    <span onClick={onToggle} className="absolute right-4 top-1/2 transform -translate-y-1/2 cursor-pointer">
      {isVisible ? <OpenEyeIcon className={iconClassName} /> : <CloseEyeIcon className={iconClassName} />}
    </span>
  );
};

export default PasswordToggle;