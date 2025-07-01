import useCategoryQuery from "@/hooks/useCategoryQuery";

export function useCategoryHref(categoryId: number) {
  const {allCategories} = useCategoryQuery();
  const categoryHref = allCategories?.results.find(item => item.id === categoryId);

  return categoryHref?.category_href
}