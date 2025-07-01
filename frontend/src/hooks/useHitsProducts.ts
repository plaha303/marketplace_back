import { hitsService } from "@/utils/packages/hitsProducts";
import { useQuery } from "@tanstack/react-query";

function useHitsProducts() {
  const { data: hitsProducts, isPending: hitsProductsPending } = useQuery({
    queryKey: ["hitsProducts"],
    queryFn: () => hitsService.getHitsProducts(),
    refetchOnWindowFocus: false
  })

  return {hitsProducts, hitsProductsPending};

}

export default useHitsProducts;