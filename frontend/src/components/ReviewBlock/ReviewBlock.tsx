import { PlatformReviewsItem } from "@/utils/packages/platformReviews/type/interface";
import { Rating } from "react-simple-star-rating";
import UserIcon from "@/assets/Icons/User.svg?react"
import { formatDate } from "@/utils/helpers/helpers";

function ReviewBlock({review}: {review: PlatformReviewsItem}) {
  return (
    <div className="review-block">
      <div className="review-block__inner">
        <div className="review-block__top md:mb-6 mb-4">
          <div className="review-block__photo rounded-full md:w-[120px] md:h-[120px] w-[56px] h-[56px]">
            {review.avatar ? (
              <img src={review.avatar} alt="" className="rounded-full" />
            ): (
              <UserIcon />
            )}
          </div>
          <div className="review-block__top-content">
            <div className="text-size-h6 text-accent-800 leading-130 font-bold md:mb-2">{review.name} {review.surname} {review.city && review.city}</div>
            <div className="text-primary-600 md:mb-2 font-secondary text-size-body-3 leading-130">{formatDate(review.created_at)}</div>
            <div className="review-block__rating">
              <Rating initialValue={review.rating} readonly />
            </div>
          </div>
        </div>

        <div className="review-block__body">
          <div className="review-block__text text-size-body-2 leading-130 text-primary-700 font-secondary truncate-multiline">
            {review.review_text}
          </div>
          <div className="review-block__more mt-4">детальніше</div>
        </div>
      </div>
    </div>
  );
}

export default ReviewBlock;