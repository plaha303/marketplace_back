import Payments1 from "@/assets/payMethods/Payments1.png"
import Payments2 from "@/assets/payMethods/Payments2.png"
import Payments3 from "@/assets/payMethods/Payments3.png"
import Payments4 from "@/assets/payMethods/Payments4.png"
import Payments5 from "@/assets/payMethods/Payments5.png"

export type PayMethodProps = {
  id: number,
  icon: string,
  label: string
}

export const payTypes: PayMethodProps[] = [
  {id: 1, icon: Payments1, label: 'Mastercard'},
  {id: 2, icon: Payments2, label: 'ApplePay'},
  {id: 3, icon: Payments3, label: 'Visa'},
  {id: 4, icon: Payments4, label: 'GooglePay'},
  {id: 5, icon: Payments5, label: 'PayPal'}
]