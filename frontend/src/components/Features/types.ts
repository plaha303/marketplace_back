import FeaturesIcons1 from '@/assets/Features/featuresIcons1.svg?react'
import FeaturesIcons2 from '@/assets/Features/featuresIcons2.svg?react'
import FeaturesIcons3 from '@/assets/Features/featuresIcons3.svg?react'
import { ComponentType, SVGProps } from 'react'

export interface FeaturesTypes {
  id: number,
  icon: ComponentType<SVGProps<SVGSVGElement>>,
  title: string,
  text: string
}

export const featuresType: FeaturesTypes[] = [
  {id: 1, icon: FeaturesIcons1, title: 'Ексклюзивність у кожному виробі', text: 'Ручна робота, яка має особливу історію та неповторний характер'},
  {id: 2, icon: FeaturesIcons2, title: 'Прямий контакт з майстрами', text: 'Спілкуйтеся безпосередньота домовляйтеся про всі нюанси замовлення'},
  {id: 3, icon: FeaturesIcons3, title: 'Живі аукціони хендмейду', text: 'Отримайте шанс придбати унікальні речі за найкращою ціною!'},
]