'use client'

import Head from "next/head";
import "./badge.css"
import { CircularProgress, CircularProgressLabel, background } from '@chakra-ui/react'

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
import { redirect, usePathname } from "next/navigation";
import useSWR from "swr";
import { Input } from "@/components/ui/input";
import { Pagination } from "@/components/ui/pagination";
import Issue from "@/app/models/issues";
import ProductIssue from '../../../models/productIssues';
import { get } from "http";
import { GetServerSideProps, InferGetServerSidePropsType } from "next";
import { fetcher } from "@/lib/products";


export interface BadgeProps {
  color: string
  text: string
}

export interface productInfo {
  value: string,
  llm_result_count: number,
  total_count: number,
}

export function Badge({ color, text} : BadgeProps) {
  return <div
    className="badge"
    style={{backgroundColor: color}}
  >
    {text}
  </div>
}

export default function Home() {

  const page = usePathname().split("/")[3];

  if (isNaN(Number(page))) {
    redirect("/404");
  } else if (Number(page) < 1) {
    redirect("/404");
  }

  const c: string[] = ["Active", "Active", "Request", "Requesting"];
  // copy the same c array 10 times
  for (let i = 0; i < 3; i++) c.push(...c);

  const allIsues: Issue[] = []

  const {data: products, isLoading, error} =  useSWR<productInfo[]>(`http://localhost:5000/aggregate_unique?field=product&page=${page}&count=20`, fetcher);

  if (isLoading || !products) return <div>Loading...</div>
  if (error) return <div>Error</div>

  const request = () => {/*TODO*/ }
  return (
    <>
      <Head>
        <title> LauzHack 2023</title>
      </Head>
      <main className="flex min-h-screen flex-col w-full p-16">
        <div className="flex items-left justify-center flex-col h-full w-full p-4 " >
          <div className="flex justify-center w-full h-24">
            <Input placeholder="Product name" className="w-[40%]"></Input>
            <Pagination pageNumber={Number(page)}></Pagination>
          </div>
          <div className="px-48">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead className="w-[4%]">Status</TableHead>
                  <TableHead className="w-[25%]">Product</TableHead>
                  <TableHead className="w-[4%]">Issues</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {products.map((product, index) => (
                  <TableRow key={index} >
                    <TableCell>
                      <Button variant="ghost" onClick={request} disabled={c[index] != "Request"}>{
                        c[index] == "Active" ? "Active" :
                          c[index] == "Request" ? "Request" :
                            <CircularProgress isIndeterminate color='gray' size={30} />
                      }</Button>
                    </TableCell>
                    <TableCell>{product.value}</TableCell>
                    <TableCell>
                      <div className="flex flex-row">
                        <Badge color="#3b81d1" text={product.total_count.toString()}/>
                        <Badge color="#d13212" text={product.total_count.toString()}/>
                        <Badge color="#ebce38" text={product.total_count.toString()}/>
                        <Badge color="#1d8102" text={product.total_count.toString()}/>
                      </div>
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