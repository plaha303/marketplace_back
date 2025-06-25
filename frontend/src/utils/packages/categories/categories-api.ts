import { request } from "@/utils/http/http-request";
import { ICategoryApi } from "./type/categories-api.interface";
import { CategoryRequestDTO, CategoryResponseDTO } from "./type/interfaces";
import { ApiEndpoint } from "@/utils/http/enums/api-endpoint";
import { HttpMethod } from "@/utils/http/enums/http-method";

class CategoryApi implements ICategoryApi {
  async getCategory(): Promise<CategoryResponseDTO> {
    return request({
      url: ApiEndpoint.CATEGORY,
      method: HttpMethod.GET
    })
  }

  async postCategory(data: CategoryRequestDTO): Promise<CategoryResponseDTO> {
    return request({
      url: ApiEndpoint.CATEGORY,
      method: HttpMethod.POST,
      body: data
    })
  }
}

export {CategoryApi}