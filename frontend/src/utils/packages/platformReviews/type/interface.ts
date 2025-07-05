export interface PlatformReviewsItem {
  id: number,
  avatar: string,
  name: string,
  surname: string,
  city: string,
  rating: number,
  review_text: string,
  created_at: string
}

export interface PlatformReviewsResponseDTO {
  count: number,
  next: string,
  previous: string,
  results: PlatformReviewsItem[]
}