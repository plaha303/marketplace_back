import { HistProductsApi } from "./hitsProducts-api";
import { HitsProductsService } from "./hitsProducts-service";

const hitsApi = new HistProductsApi();
const hitsService = new HitsProductsService(hitsApi);

export {hitsService};