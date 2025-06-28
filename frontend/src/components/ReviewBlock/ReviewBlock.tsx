import { Rating } from "react-simple-star-rating";

function ReviewBlock() {
  return (
    <div className="review-block">
      <div className="review-block__inner">
        <div className="review-block__top md:mb-6 mb-4">
          <div className="review-block__photo rounded-full md:w-[120px] md:h-[120px] w-[56px] h-[56px]">
            <img src="" alt="" className="rounded-full" />
          </div>
          <div className="review-block__top-content">
            <div className="text-size-h6 text-accent-800 leading-130 font-bold md:mb-2">Олена М., Київ</div>
            <div className="text-primary-600 md:mb-2 font-secondary text-size-body-3 leading-130">08/05/24</div>
            <div className="review-block__rating">
              <Rating />
            </div>
          </div>
        </div>

        <div className="review-block__body">
          <div className="review-block__text text-size-body-2 leading-130 text-primary-700 font-secondary truncate-multiline">
            Знайшла тут ідеальний подарунок – унікальний хендмейд-гаманець! 
            Приємно, що можна поспілкуватися безпосередньо з 
          </div>
          <div className="review-block__more mt-4">детальніше</div>
        </div>
      </div>
    </div>
  );
}

export default ReviewBlock;