import { platformReviewsService } from "@/utils/packages/platformReviews";
import { useQuery } from "@tanstack/react-query";

function usePlatformReviewsQuery() {
  const {data: allPlatformReviews, isPending: allPlatformReviewsPending} = useQuery({
    queryKey: ["platformReviews"],
    queryFn: () => platformReviewsService.getPlatformReviews(),
    refetchOnWindowFocus: false,
    retry: false
  })

  return {allPlatformReviews, allPlatformReviewsPending}
}

export default usePlatformReviewsQuery;