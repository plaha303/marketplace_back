import { ProductCardAuctionProps } from "@/components/ProductCard/types/interface";

import ProductCardAuction1 from "@/assets/ProductCardAuction/ProductCardAuction1.png"
import ProductCardAuction2 from "@/assets/ProductCardAuction/ProductCardAuction2.png"
import ProductCardAuction3 from "@/assets/ProductCardAuction/ProductCardAuction3.png"
import ProductCardAuction4 from "@/assets/ProductCardAuction/ProductCardAuction4.png"

export const productsAuction: ProductCardAuctionProps[] = [
  {
    id: 1,
    vendor: {
      id: 1,
      username: 'Dasha',
      email: 'text@text.com',
      role: ["user"],
    },
    category: 1,
    name: 'Ваза із глини, ручна ліпка',
    description: 'some description',
    sale_type: 'auction',
    price: 100,
    start_price: 50,
    auction_end_time: '2025-06-23T12:28:12.775Z',
    stock: 1,
    created_at: '2025-06-21T12:28:12.775Z',
    images: [
      {
        id: 1,
        image_url: ProductCardAuction1,
      }
    ],
    product_href: "D11JW2kEXcNQPD_ZKG937qtSKFkjtPpK7BmUQonBzL"
  }, 
  {
    id: 2,
    vendor: {
      id: 1,
      username: 'Dasha 2',
      email: 'text2@text.com',
      role: ["user"],
    },
    category: 1,
    name: 'Lorem Ipsum is simply dummy text of the printing and typesetting industry',
    description: 'some description',
    sale_type: 'auction',
    price: 200,
    start_price: 150,
    auction_end_time: '2025-06-23T12:28:12.775Z',
    stock: 2,
    created_at: '2025-06-21T12:28:12.775Z',
    images: [
      {
        id: 1,
        image_url: ProductCardAuction2
      }
    ],
    product_href: "D11JW2kEXcNQPD_ZKG937qtSKFkjtPpK7BmUQonBzL"
  }, 
  {
    id: 3,
    vendor: {
      id: 1,
      username: 'Dasha 3',
      email: 'text3@text.com',
      role: ["user"],
    },
    category: 1,
    name: 'Product 3',
    description: 'some description',
    sale_type: 'auction',
    price: 250,
    start_price: 150,
    auction_end_time: '2025-06-23T12:28:12.775Z',
    stock: 2,
    created_at: '2025-06-21T12:28:12.775Z',
    images: [
      {
        id: 1,
        image_url: ProductCardAuction3
      }
    ],
    product_href: "D11JW2kEXcNQPD_ZKG937qtSKFkjtPpK7BmUQonBzL"
  }, 
  {
    id: 4,
    vendor: {
      id: 1,
      username: 'Dasha 4',
      email: 'text3@text.com',
      role: ["user"],
    },
    category: 1,
    name: 'Product 4',
    description: 'some description',
    sale_type: 'auction',
    price: 350,
    start_price: 350,
    auction_end_time: '2025-06-23T12:28:12.775Z',
    stock: 2,
    created_at: '2025-06-21T12:28:12.775Z',
    images: [
      {
        id: 1,
        image_url: ProductCardAuction4
      }
    ],
    product_href: "D11JW2kEXcNQPD_ZKG937qtSKFkjtPpK7BmUQonBzL"
  }, 
]