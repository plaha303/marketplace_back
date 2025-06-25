const ApiEndpoint = {
  LOGIN: '/auth/login/',
  SIGNUP: '/auth/register/',
  EMAILCONFIRM: '/auth/verify-email/',
  REFRESHTOKEN: '/auth/refresh/',

  CATEGORY: '/categories'
} as const

type ApiEndpoint = typeof ApiEndpoint[keyof typeof ApiEndpoint]

export {ApiEndpoint}