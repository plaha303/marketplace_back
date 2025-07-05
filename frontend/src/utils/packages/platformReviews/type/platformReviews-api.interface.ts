import { PlatformReviewsResponseDTO } from "./interface"

interface IPlatformReviewsApi {
  getPlatformReviews: () => Promise<PlatformReviewsResponseDTO>
}

export { type IPlatformReviewsApi}