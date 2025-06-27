import { Link } from "react-router";

interface SliderWithReviewsProps {
  title: string;
  watchAll: string
}

function SliderWithReviews({title, watchAll}: SliderWithReviewsProps) {
  return (
    <div className="slider-review">
      <div className="container px-4 mx-auto">
        <div className="slider-review__header lg:mb-16 mb-9 flex items-center justify-between md:flex-row flex-col md:gap-0 gap-4">
          <h3 className="m:text-size-h3 text-size-h2 uppercase text-accent-800 font-bold leading-130">{title}</h3>
          <Link to={watchAll} className="font-secondary underline text-size-body-3 leading-100 text-primary-600">дивитися всі</Link>
        </div>
        <div className="slider-review__body">

        </div>
      </div>
    </div>
  );
}

export default SliderWithReviews;