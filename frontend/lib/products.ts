import Issue from "@/app/models/issues";
import ProductIssue from "@/app/models/productIssues";
import useSWR, { SWRResponse } from "swr";

export async function fetcher<JSON = any>(
    input: RequestInfo,
    init?: RequestInit
  ): Promise<JSON> {
    const res = await fetch(input, init)
    return res.json()
  }



export function getProductNames(page: number = 1){
    return useSWR<string[]>(`http://localhost:5000/issues?page=${page}`, fetcher);
}

export function getIssues() {
    return useSWR<Issue[]>(`http://localhost:5000/issues`, fetcher);
}

export function combineProductNamesAndIssues(p: string[], i: Issue[]) {
    var data: {[key: string]: ProductIssue} = {}
    for (var product in p) {
        data[product] = {
            status: "Request",
            issues: 0,
            high: 0,
            low: 0,
            medium: 0
        }
    }
    i.forEach((issue) => {
        if (issue.example.product in p) {
            data[issue.example.product].issues += 1;
        }
    })
}