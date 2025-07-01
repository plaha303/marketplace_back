import { getHitsResponseDTO } from "./interface"


interface IHitsProductsService {
  getHitsProducts: () => Promise<getHitsResponseDTO>
}

export {IHitsProductsService}