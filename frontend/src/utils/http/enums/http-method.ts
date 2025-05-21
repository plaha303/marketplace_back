const HttpMethod = {
  GET: 'GET',
  POST: 'POST',
  PUT: 'PUT',
  DELETE: 'DELETE',
  PATCH: 'PATCH'
} as const

type HttpMethod = typeof HttpMethod[keyof typeof HttpMethod]

export {HttpMethod}