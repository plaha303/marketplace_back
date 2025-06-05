import { IconProps } from './type/interface';

function LogoIcon({color="currentColor", size="40"}: IconProps) {
  return (
    <svg width={size} height="56" viewBox="0 0 40 56" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M7.88247 54.4871L4.88054 27.5237H22.3796L32.4836 39.3935L4.88054 27.5237L18.5722 42.1777L7.88247 54.4871Z" fill={color}/>
      <path d="M4.88054 27.5237L1 35.0706L7.73603 55L18.6455 42.251L28.9692 54.3406L32.5568 39.3935V14.2619L39 13.0896V10.3786L34.6069 7.81411L37.5356 2.31886L31.605 6.78833L33.8748 1L26.6994 6.78833L22.3796 27.5237M4.88054 27.5237H22.3796M4.88054 27.5237L7.88247 54.4871L18.5722 42.1777L4.88054 27.5237ZM4.88054 27.5237L32.4836 39.3935L22.3796 27.5237" stroke={color} strokeLinejoin="round"/>
    </svg>
  );
}

export default LogoIcon;