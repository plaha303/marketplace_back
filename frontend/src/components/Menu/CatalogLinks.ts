
import Category1 from '@/assets/category/category-1.png'
import Category2 from '@/assets/category/category-2.png'
import Category3 from '@/assets/category/category-3.png'
import Category4 from '@/assets/category/category-4.png'
import Category5 from '@/assets/category/category-5.png'
import Category6 from '@/assets/category/category-6.png'
import Category7 from '@/assets/category/category-7.png'
import Category8 from '@/assets/category/category-8.png'
import Category9 from '@/assets/category/category-9.png'
import Category10 from '@/assets/category/category-10.png'
import Category11 from '@/assets/category/category-11.png'
import Category from "@/routers/enums/category";

const catalogLinks = [
  {id: 1, label: 'Мистецтво та декор', icon: Category1, categoryId: Category.ART_DECOR },
  {id: 2, label: 'Дитячі товари', icon: Category2, categoryId: Category.BABY_PRODUCTS },
  {id: 3, label: 'Предмети дому', icon: Category3, categoryId: Category.HOME_GOODS },
  {id: 4, label: 'Прикраси та аксесуари', icon: Category4, categoryId: Category.JEWELRY_ACCESSORIES },
  {id: 5, label: 'Аромати та свічки', icon: Category5, categoryId: Category.FRAGRANCE_CANDLES },
  {id: 6, label: 'Сумки та гаманці', icon: Category6, categoryId: Category.BAGS_WALLETS },
  {id: 7, label: 'Одяг та текстиль', icon: Category7, categoryId: Category.CLOTHING_TEXTILES },
  {id: 8, label: 'Святковий декор', icon: Category8, categoryId: Category.HOLIDAY_DECOR },
  {id: 9, label: 'Для неї', icon: Category9, categoryId: Category.FOR_HER },
  {id: 10, label: 'Для нього', icon: Category10, categoryId: Category.FOR_HIM },
  {id: 11, label: 'Різне', icon: Category11, categoryId: Category.DIFFERENT },
] as const;

export default catalogLinks;