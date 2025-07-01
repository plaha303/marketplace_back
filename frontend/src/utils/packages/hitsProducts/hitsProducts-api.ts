
import { IHitsProductsApi } from "./type/hitsProducts-api.interface";
import { request } from "@/utils/http/http-request";
import { HttpMethod } from "@/utils/http/enums/http-method";
import { ApiEndpoint } from "@/utils/http/enums/api-endpoint";
import { getHitsResponseDTO } from "./type/interface";


class HistProductsApi implements IHitsProductsApi {
  async getHitsProducts(): Promise<getHitsResponseDTO> {
    return request({
      method: HttpMethod.GET,
      url: ApiEndpoint.GETHiTS,
    })
  }
}

export {HistProductsApi}