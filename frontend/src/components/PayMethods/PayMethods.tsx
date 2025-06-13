import { payTypes } from "./interfaces";

function PayMethods() {
  return (
    <div className="payMethods">
      <div className="payMethods__items flex items-center gap-3">
        {payTypes.map(pay => (
          <div className="payMethods__item" key={pay.id}>
            <span>
              <img src={pay.icon} alt={pay.label} title={pay.label} />
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

export default PayMethods;