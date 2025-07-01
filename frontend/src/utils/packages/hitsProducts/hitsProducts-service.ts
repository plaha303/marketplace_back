import { IHitsProductsApi } from "./type/hitsProducts-api.interface";
import { IHitsProductsService } from "./type/hitsProducts-service.interface";
import { getHitsResponseDTO } from "./type/interface";

class HitsProductsService implements IHitsProductsService {
  private hitsApi: IHitsProductsApi;

  constructor(hitsApi: IHitsProductsApi) {
    this.hitsApi = hitsApi
  }

  async getHitsProducts(): Promise<getHitsResponseDTO>  {
    return this.hitsApi.getHitsProducts()
  }

}

export {HitsProductsService}