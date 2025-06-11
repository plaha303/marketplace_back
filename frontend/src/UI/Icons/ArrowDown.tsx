import { IconProps } from './type/interface';

function ArrowDown({className}: IconProps) {
  return (
    <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg" className={className}>
      <path d="M16.25 7.5L10 13.75L3.75 7.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
    </svg>

  );
}

export default ArrowDown;