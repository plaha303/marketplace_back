import axios from "axios";
import { Request } from "../../http/http-request-service";
import { HttpMethod } from "../../http/enums/http-method";
import { ApiEndpoint } from "../../http/enums/api-endpoint";

export interface LogInProps {
  email: string,
  password: string
}

export async function LogIn(data: LogInProps) {
  return Request({
    url: ApiEndpoint.LOGIN,
    method: HttpMethod.POST,
    body: data
  })
}
