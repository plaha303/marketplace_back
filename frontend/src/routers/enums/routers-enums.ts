const AppRoute = {
  ROOT: '/',
  ABOUT: '/about',
  CONTACT: '/contact',
  SUPPORT: '/support',

  REGISTRATION: '/registration',
  SENDCONFIRMLETTER: '/confirm_email',
  VERIFYEMAIL: '/verify-email/:uid/:token',
  LOGIN: '/login',
  RESET_PASSWORD: '/reset_password',

  HITS: '/hits',


  PROFILE: '/profile',
  MASTER: '/master',
  ORDERS: '/orders',
  GOODS: '/goods',
  FAVORITE: '/favorite',
  NOTIFICATION: '/notification',
  MESSAGES: '/messages',
  REVIEWS: '/reviews',
  SETTINGS: '/settings',
  BASKET: '/basket',
  BLOG: '/blog',
  CATEGORY: '/:category',
  PRIVACY_POLICY: '/privacy_policy',
  PROCESSING_PERSONAL_DATA: '/processing_personal_data',
  TERMS_SERVICE: '/terms_of_service'
} as const;

type AppRoute = (typeof AppRoute)[keyof typeof AppRoute];

export default AppRoute;