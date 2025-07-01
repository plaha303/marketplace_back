export interface ProductImages {
  id: number;
  image_url: string;
}

export interface ProductDTO { 
  id: number;
  vendor: {
    id: number;
    username: string;
    email: string;
    role: string[];
  }
  category: number;
  name: string;
  description: string;
  sale_type: string;
  price: number;
  stock: number;
  created_at: string;
  images: ProductImages[],
  product_href: string,
  start_price: number;
  auction_end_time: string;
  discount_price: string;
  reviews_count: number;
  rating: number;
}

export interface getHitsResponseDTO { 
  message: string;
  success: boolean;
  results: ProductDTO[];
}