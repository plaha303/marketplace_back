import { PlatformReviewsItem } from "@/utils/packages/platformReviews/type/interface";
import { Rating } from "react-simple-star-rating";
import UserIcon from "@/assets/Icons/User.svg?react"
import { formatDate } from "@/utils/helpers/helpers";
import { useEffect, useRef, useState } from "react";
import classNames from "classnames";

import style from './ReviewBlock.module.scss'

function ReviewBlock({review}: {review: PlatformReviewsItem}) {
  const shortSurName = review.surname.charAt(0);
  const [isExpanded, setIsExpanded] = useState(false)
  const [isTruncated, setIsTruncated] = useState(false)
  const textReview = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const element = textReview.current;
    if (element) {
      const lineHeight = parseFloat(getComputedStyle(element).lineHeight || "0");
      const lines = Math.round(element.scrollHeight / lineHeight);

      setIsTruncated(lines > 3);
    }
  }, [review.review_text]);

  return (
    <div className="review-block">
      <div className="review-block__inner p-6 rounded-4xl shadow-custom1">
        <div className="review-block__top md:mb-6 mb-4 flex items-center gap-6">
          <div className="review-block__photo rounded-full md:w-[120px] md:h-[120px] w-[56px] h-[56px]">
            {review.avatar ? (
              <img src={review.avatar} alt="" className="rounded-full" />
            ): (
              <UserIcon />
            )}
          </div>
          <div className="review-block__top-content">
            <div className="text-size-h6 text-accent-800 leading-130 font-bold md:mb-2">{review.name} {shortSurName}, {review.city && review.city}</div>
            <div className="text-primary-600 md:mb-2 font-secondary text-size-body-3 leading-130">{formatDate(review.created_at)}</div>
            <div className="review-block__rating">
              <Rating initialValue={review.rating} readonly fillColor="#A0864D" className="flex" size={20} SVGclassName="inline" />
            </div>
          </div>
        </div>

        <div className="review-block__body">
          <div ref={textReview} className={classNames('review-block__text text-size-body-2 leading-130 text-primary-700 font-secondary truncate-multiline', 
          !isExpanded && 'truncate-multiline')}>
            {review.review_text}
          </div>

          {isTruncated && (
            <div className="review-block__more mt-4" onClick={() => setIsExpanded(prev => !prev)}>
              {isExpanded ? 'згорнути' : 'детальніше'} 
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default ReviewBlock;