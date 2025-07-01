import { ProductDTO } from "@/utils/packages/hitsProducts/type/interface";

export interface SliderWithProductsProps {
  title: string;
  watchAll: string;
  data: ProductDTO[];
}