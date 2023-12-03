'use client'

import Head from "next/head";
import "./badge.css"
import { CircularProgress, CircularProgressLabel, background, useQuery } from '@chakra-ui/react'

import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { Button } from "@/components/ui/button";
import { redirect, useParams, usePathname, useSearchParams } from "next/navigation";
import useSWR from "swr";
import { Input } from "@/components/ui/input";
import { Pagination } from "@/components/ui/pagination";
import { get } from "http";
import { GetServerSideProps, InferGetServerSidePropsType } from "next";
import { productInfo } from "@/app/models/models";
import { fetcher } from "@/lib/utils";
import { useState } from "react";
import ProductIssue from '@/app/models/productIssues';


export interface BadgeProps {
  color: string
  text: string
}


export function Badge({ color, text }: BadgeProps) {
  return <div
    className="badge"
    style={{ backgroundColor: color }}
  >
    {text}
  </div>
}


const ReloadAfterApiRequestButton = ({ product }: { product: string }) => {
  const [isLoading, setIsLoading] = useState(false);

  const fetchDataAndReload = async () => {
    try {
      setIsLoading(true);


      // Send an API request
      const response = await fetch(`http://localhost:5000/issues?product=${encodeURIComponent(product)}`);

      // Handle the response if needed

      // Reload the page
    } catch (error) {
      console.error('Error sending API request:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div>
      <button onClick={fetchDataAndReload} disabled={isLoading}>
        {isLoading ? 'Loading...' : 'Send API Request and Reload'}
      </button>
    </div>
  );
};



export default function Home() {

  const page = useParams().pageNumber;
  const searchQuery = useSearchParams().get("search") ?? "";
  const [search, setSearch] = useState<string>(searchQuery);
  const [isRequesting, setIsRequesting] = useState<boolean>(false);

  if (isNaN(Number(page))) {
    redirect("/404");
  } else if (Number(page) < 1) {
    redirect("/404");
  }

  const updateSearch = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSearch(event.target.value);
  }

  // formhanlder on saerch
  const handleSearch = () => {
    redirect(`/products/page/${page}?search=${search}`);
  }

  const { data: products, isLoading, error } = useSWR<productInfo[]>(`http://localhost:5000/aggregate_unique?field=product&page=${page}&count=5`, fetcher);

  if (isLoading || !products) return <div>Loading...</div>
  if (error) return <div>Error</div>

  const handleClick = (product: ProductIssue) => async () => {
    setIsRequesting(true);
    try {
      product.llm_result_count = -1;
      const response = await fetch(`http://localhost:5000/issues?product=${encodeURIComponent(product.value)}`);
      const data = await response.json();
    } catch (error) {
      console.error('Error sending API request:', error);
    } finally {
      setIsRequesting(false);
      window.location.reload();
    }
  }

  return (
    <>
      <Head>
        <title> LauzHack 2023</title>
      </Head>
      <main className="flex min-h-screen flex-col w-full p-16">
        <div className="flex items-left justify-center flex-col h-full w-full p-4 " >
          <div className="flex justify-center w-full h-24">
            <form action={`/products/page/1/?search=${search}`} className="w-[40%]" method="get" >
              <Input type="search" placeholder="Product name" className="w-full" value={search} onChange={updateSearch}></Input>
            </form>
            <Pagination pageNumber={Number(page)}></Pagination>
          </div>
          <div className="px-48">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead className="w-[3%]">Status</TableHead>
                  <TableHead className="w-[28%]">Product</TableHead>
                  <TableHead className="w-[3%]">Issues</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {products.map((product, index) => (
                  <TableRow key={index}>
                    <TableCell className="py-[0.39rem]">
                      {
                        isRequesting && product.llm_result_count == -1 ? <CircularProgress className = "ml-7" isIndeterminate size="24px" /> :
                          <Button variant="ghost" onClick={handleClick(product)} disabled={product.llm_result_count != 0}>
                            {product.llm_result_count != 0 ? "Active" : "Request"}
                          </Button>
                      }
                    </TableCell>
                    <TableCell className="py-[0.39rem]">{product.value}</TableCell>
                    <TableCell className="py-[0.39rem]">
                      {product.llm_result_count > 0 ?
                        <div className="flex flex-row">
                          <Badge color="#d13212" text={product.severities.high.toString()} />
                          <Badge color="#ebce38" text={product.severities.medium.toString()} />
                          <Badge color="#1d8102" text={product.severities.low.toString()} />
                        </div> : "Request"
                      }
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        </div>
      </main>
    </>
  );
}