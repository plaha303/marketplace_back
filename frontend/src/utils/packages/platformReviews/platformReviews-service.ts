import { PlatformReviewsResponseDTO } from "./type/interface";
import { IPlatformReviewsApi } from "./type/platformReviews-api.interface";
import { IPlatformReviewsService } from "./type/platformReviews-service.interface";

class PlatformReviewService implements IPlatformReviewsService {
  private platformReviewsApi: IPlatformReviewsApi;

  constructor(platformReviewsApi: IPlatformReviewsApi) {
    this.platformReviewsApi = platformReviewsApi;
  }

  async getPlatformReviews(): Promise<PlatformReviewsResponseDTO> {
    return this.platformReviewsApi.getPlatformReviews();
  }
}

export {PlatformReviewService}