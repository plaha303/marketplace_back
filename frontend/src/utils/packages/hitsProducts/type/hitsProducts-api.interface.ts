import { getHitsResponseDTO } from "./interface"


interface IHitsProductsApi {
  getHitsProducts: () => Promise<getHitsResponseDTO>
}

export {IHitsProductsApi}