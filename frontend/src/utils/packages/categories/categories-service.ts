import { ICategoryApi } from "./type/categories-api.interface";
import { ICategoryService } from "./type/categories-service.interface";
import { CategoryRequestDTO, CategoryResponseDTO } from "./type/interfaces";

class CategoryService implements ICategoryService {
  private categoryApi: ICategoryApi;
  
  constructor(categoryApi: ICategoryApi) {
    this.categoryApi = categoryApi;
  }

  async getCategory(): Promise<CategoryResponseDTO> {
    return this.categoryApi.getCategory()
  }

  async postCategory(data: CategoryRequestDTO): Promise<CategoryResponseDTO> {
    return this.categoryApi.postCategory(data);
  }
}

export {CategoryService}