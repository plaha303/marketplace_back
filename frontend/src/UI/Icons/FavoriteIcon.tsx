import { IconProps } from './type/interface';

function FavoriteIcon({className=''}: IconProps) {
  return (
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" className={className}>
      <path d="M12 20.25C12 20.25 2.625 15 2.625 8.625C2.62519 7.49825 3.01561 6.40634 3.72989 5.53492C4.44416 4.6635 5.4382 4.06635 6.54299 3.84501C7.64778 3.62366 8.79514 3.79178 9.78999 4.32078C10.7848 4.84978 11.5658 5.70701 12 6.74672L12 6.74673C12.4342 5.70701 13.2152 4.84979 14.21 4.32078C15.2049 3.79178 16.3522 3.62366 17.457 3.84501C18.5618 4.06635 19.5558 4.6635 20.2701 5.53492C20.9844 6.40634 21.3748 7.49825 21.375 8.625C21.375 15 12 20.25 12 20.25Z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
    </svg>

  );
}

export default FavoriteIcon;