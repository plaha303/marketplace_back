import { PlatformReviewApi } from "./platformReviews-api";
import { PlatformReviewService } from "./platformReviews-service";

const platformReviewsApi = new PlatformReviewApi();
const platformReviewsService = new PlatformReviewService(platformReviewsApi);

export {platformReviewsService}