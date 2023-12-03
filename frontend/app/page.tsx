"use client";

import { Button } from "@/components/ui/button";
import Header from "@/components/ui/header";
import Link from "next/link";

import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import useSWR, { mutate } from "swr";
import { fetcher } from "@/lib/utils";

interface brandInfo {
  value: string,
  total_count: number,
  llm_result_count: number,
}

export default function Home() {

  var { data: brands, isLoading, error } = useSWR<brandInfo[]>(`http://localhost:5000/aggregate_unique?field=brand&page=1&count=200`, fetcher);

  if (isLoading || !brands) return <div>Loading...</div>
  if (error) return <div>Error </div>

  // sum of totalcount of all brands
  const sum = brands.reduce((a, b) => a + b.total_count, 0);

  brands = [{value: "All brands", total_count: sum, llm_result_count: 0}, ...brands]

  return (
    <>
      <Header />
      <div className="absolute min-h-screen grid grid-cols-4 grid-flow-row gap-3 min-w-[100vw] mt-20 p-8">
        {/* 4 x 4 grid of Cards */}
        {brands.map((brand, index) => (
          <Link href={`${encodeURIComponent(brand.value == "" ? "All brands" : brand.value)}/products/page/1`}>
            <Card key={index} className = "border-gray-800">
              <CardHeader>
                <CardTitle className = "font-bold">{brand.value == "" ? "No Brand" : brand.value}</CardTitle>
              </CardHeader>
              <CardContent>
                <p>Issues: {brand.total_count}</p>
              </CardContent>
            </Card>
          </Link>
        ))}
      </div>

    </>
  );
}