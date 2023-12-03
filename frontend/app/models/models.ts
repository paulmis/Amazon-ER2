// api/aggregate_query?field=product
export interface productInfo {
    value: string,
    llm_result_count: number,
    total_count: number,
    severities: {
      high: number,
      medium: number,
      low: number,
    }
  }

  export interface Comment {
    id: number;
    product: string;
    brand: string;
    price: number;
    rating: number;
    review: string;
    votes: number;
}

