import { PlatformReviewsResponseDTO } from "./interface";

interface IPlatformReviewsService {
  getPlatformReviews: () => Promise<PlatformReviewsResponseDTO>
}

export {type IPlatformReviewsService}