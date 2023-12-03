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

export type Severity = "low" | "medium" | "high"

export interface Comment {
  id: number;
  product: string;
  brand: string;
  price: number;
  rating: number;
  review: string;
  votes: number;
}

export interface Issue {
  /**
   * LLM-generated description of the issue.
   */
  comment: string

  /**
   * The confidence score of the detection.
   */
  confidence: number

  /**
   * The type of the issue.
   */
  issue: string

  /**
   * {@link Severity} of the issue.
   */
  severity: Severity
}

export interface IssueCluster {
  /**
   * The name of the cluster.
   */
  name: string

  /**
   * The issues that belong to this cluster.
   */
  issues: string[]

  /**
   * Number of reviews.
   */
  item_count: number

  /**
   * Example review.
   */
  example: Comment
}

