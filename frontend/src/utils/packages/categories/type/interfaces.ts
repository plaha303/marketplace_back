export interface Category {
  id: number;
  name: string;
  parent: number;
  category_image: string;
  category_href: string;
}

export interface CategoryResponseDTO {
  count: number;
  next: string;
  previous: string;
  results: Category[];
}

export interface CategoryRequestDTO {
  name: string;
  parent: number;
  category_image: string;
  category_href: string;
}