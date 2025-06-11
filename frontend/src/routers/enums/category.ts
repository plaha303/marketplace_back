const Category = {
  ART_DECOR: 0,
  BABY_PRODUCTS: 1,
  HOME_GOODS: 2,
  JEWELRY_ACCESSORIES: 3,
  FRAGRANCE_CANDLES: 4,
  BAGS_WALLETS: 5,
  CLOTHING_TEXTILES: 6,
  HOLIDAY_DECOR: 7,
  FOR_HER: 8,
  FOR_HIM: 9,
  DIFFERENT: 10
} as const 

type Category = (typeof Category)[keyof typeof Category];

export default Category;

export const CategorySlugMap: Record<Category, string> = {
  0: 'art_decor',
  1: 'baby_products',
  2: 'home_goods',
  3: 'jewelry_accessories',
  4: 'fragrance_candles',
  5: 'bags_wallets',
  6: 'clothing_textiles',
  7: 'holiday_decor',
  8: 'for_her',
  9: 'for_him',
  10: 'different'
};

export const SlugCategoryMapping = Object.entries(CategorySlugMap).reduce((acc, [key, slug]) => {
  acc[slug] = Number(key) as Category;
  return acc
}, {} as Record<string, Category>)