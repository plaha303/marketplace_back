const ApiEndpoint = {
  LOGIN: '/auth/login/',
  SIGNUP: '/auth/register/',
  VERIFYEMAIL: '/auth/verify-email',
  REFRESHTOKEN: '/auth/refresh/',

  CATEGORY: '/categories',
  GETHiTS: '/hits'
} as const

type ApiEndpoint = typeof ApiEndpoint[keyof typeof ApiEndpoint]

export {ApiEndpoint}