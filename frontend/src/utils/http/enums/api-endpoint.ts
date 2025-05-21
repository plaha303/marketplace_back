const ApiEndpoint = {
  LOGIN: '/auth/login/',
  SINGUP: '/auth/register/',
  EMAILCONFIRM: '/auth/verify-email/',
  REFRESHTOKEN: '/auth/refresh/'
} as const

type ApiEndpoint = typeof ApiEndpoint[keyof typeof ApiEndpoint]

export {ApiEndpoint}