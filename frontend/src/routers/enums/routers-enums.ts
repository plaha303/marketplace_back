const AppRoute = {
  ROOT: '/',
  ABOUT: '/about',
  CONTACT: '/contact',
  SUPPORT: '/support',
  REGISTRATION: '/registration',
  LOGIN: '/login',
  LOGOUT: '/logout',
  PROFILE: '/profile',
  FAVORITE: '/favorite',
  NOTIFICATION: '/notification',
  BASKET: '/basket',
  BLOG: '/blog',
  CATEGORY: '/:category'
} as const;

type AppRoute = (typeof AppRoute)[keyof typeof AppRoute];

export default AppRoute;