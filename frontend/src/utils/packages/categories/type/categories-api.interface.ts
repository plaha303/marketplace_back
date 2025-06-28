import { CategoryRequestDTO, CategoryResponseDTO } from "./interfaces";

interface ICategoryApi {
  getCategory: () => Promise<CategoryResponseDTO>
  postCategory: (data: CategoryRequestDTO) => Promise<CategoryResponseDTO>
}

export {type ICategoryApi}