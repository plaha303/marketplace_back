import { CategoryApi } from "./categories-api";
import { CategoryService } from "./categories-service";

const categoryApi = new CategoryApi();
const categoryService = new CategoryService(categoryApi);

export {categoryService}