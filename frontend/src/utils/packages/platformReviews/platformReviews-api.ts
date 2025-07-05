import { request } from "@/utils/http/http-request";
import { PlatformReviewsResponseDTO } from "./type/interface";
import { IPlatformReviewsApi } from "./type/platformReviews-api.interface";
import { ApiEndpoint } from "@/utils/http/enums/api-endpoint";
import { HttpMethod } from "@/utils/http/enums/http-method";

class PlatformReviewApi implements IPlatformReviewsApi {
  async getPlatformReviews(): Promise<PlatformReviewsResponseDTO> {
    return request({
      url: ApiEndpoint.PLATFORMREVIEWS,
      method: HttpMethod.GET
    })
  }
}

export {PlatformReviewApi}