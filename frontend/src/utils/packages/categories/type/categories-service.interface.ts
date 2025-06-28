import { CategoryRequestDTO, CategoryResponseDTO } from "./interfaces";

interface ICategoryService {
  getCategory: () => Promise<CategoryResponseDTO>
  postCategory: (data: CategoryRequestDTO) => Promise<CategoryResponseDTO>
}

export {type ICategoryService}