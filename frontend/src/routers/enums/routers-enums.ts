const AppRoute = {
  ROOT: '/',
  ABOUT: '/about',
  CONTACT: '/contact',
  SUPPORT: '/support',

  REGISTRATION: '/registration',
  CONFIRM_EMAIL: '/confirm_email',
  SUCCESSFULLY_EMAIL_CONFIRM: '/confirm_email_done',
  LOGIN: '/login',
  LOGOUT: '/logout',
  RESET_PASSWORD: '/reset_password',


  PROFILE: '/profile',
  FAVORITE: '/favorite',
  NOTIFICATION: '/notification',
  BASKET: '/basket',
  BLOG: '/blog',
  CATEGORY: '/:category',
  PRIVACY_POLICY: '/privacy_policy',
  PROCESSING_PERSONAL_DATA: '/processing_personal_data',
  TERMS_SERVICE: '/terms_of_service'
} as const;

type AppRoute = (typeof AppRoute)[keyof typeof AppRoute];

export default AppRoute;