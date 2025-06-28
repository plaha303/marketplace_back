import { categoryService } from "@/utils/packages/categories";
import { useQuery } from "@tanstack/react-query";

function useCategoryQuery() {
  const {data: allCategories, isPending} = useQuery({
    queryKey: ['category'],
    queryFn: () => categoryService.getCategory(),
    refetchOnWindowFocus: false
  })

  return {allCategories, isPending};
}

export default useCategoryQuery;