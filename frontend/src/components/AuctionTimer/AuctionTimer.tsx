import { formatTimeForAuction } from "@/utils/helpers/helpers";

function AuctionTimer({time}: {time: string}) {
  const { hours, minutes, seconds } = formatTimeForAuction(time);

  return (
    <div className="flex md:gap-2 gap-1">
      <div className="timer-block p-2 md:w-14 md:h-14 w-11 h-11 rounded-2xl text-center bg-accent-100">
        <div className="timer-block__top leading-100 text-accent-800 md:text-size-card-1 text-size-body-3">
          {hours}
        </div>
        <div className="timer-block__bottom text-primary-700 font-secondary  md:text-size-card-3 text-size-body-5 leading-100">год</div>
      </div>

      <div className="timer-block p-2 md:w-14 md:h-14 w-11 h-11 rounded-2xl text-center bg-accent-100">
        <div className="timer-block__top leading-100 text-accent-800 md:text-size-card-1 text-size-body-3">
          {minutes}
        </div>
        <div className="timer-block__bottom text-primary-700 font-secondary  md:text-size-card-3 text-size-body-5 leading-100">хв</div>
      </div>

      <div className="timer-block p-2 md:w-14 md:h-14 w-11 h-11 rounded-2xl text-center bg-accent-100">
        <div className="timer-block__top leading-100 text-accent-800 md:text-size-card-1 text-size-body-3">
          {seconds}
        </div>
        <div className="timer-block__bottom text-primary-700 font-secondary  md:text-size-card-3 text-size-body-5 leading-100">сек</div>
      </div>
    </div>
  );
}

export default AuctionTimer;