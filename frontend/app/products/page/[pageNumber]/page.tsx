'use client'

import Head from "next/head";
import Link from "next/link";
import { CircularProgress, CircularProgressLabel } from '@chakra-ui/react'

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
import { Product } from "@/app/models/product";
import useSWR from "swr";
import { Input } from "@/components/ui/input";
import { Pagination } from "@/components/ui/pagination";

export async function fetcher<JSON = any>(
  input: RequestInfo,
  init?: RequestInit
): Promise<JSON> {
  const res = await fetch(input, init)
  return res.json()
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

  var { data, error, isLoading } = useSWR(`http://localhost:5000/aggregate_unique?page=${page}`, fetcher);
  if (isLoading) return <div>Loading...</div>
  if (error) return <div>Error</div>

  const products = data as string[];
  console.log(data);

  const request = () => {/*TODO*/ }
  return (
    <>
      <Head>
        <title> LauzHack 2023</title>
      </Head>
      <main className="flex min-h-screen flex-col w-full p-16">
        <div className="flex items-center justify-center flex-col h-full w-full p-4 " >
          <div className="flex justify-center w-full h-24">
            <Input placeholder="Search" className="w-[50%]"></Input>
            <Pagination pageNumber={Number(page)}></Pagination>
          </div>
          <div className="w-full px-48">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead className="w-[7%]">Status</TableHead>
                  <TableHead className="w-[20%]">Product</TableHead>
                  <TableHead className="w-[12%]">Issues</TableHead>
                  <TableHead className="w-[7%]">High</TableHead>
                  <TableHead className="w-[7%]">Med</TableHead>
                  <TableHead className="w-[7%]">Low</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {products.map((product, index) => (
                  <TableRow key={index}>
                    <TableCell>
                      <Button variant="ghost" onClick={request} disabled={c[index] != "Request"}>{
                        c[index] == "Active" ? "Active" :
                          c[index] == "Request" ? "Request" :
                            <CircularProgress isIndeterminate color='gray' size={30} />
                      }</Button>
                    </TableCell>
                    <TableCell>{product}</TableCell>
                    <TableCell>42</TableCell>
                    <TableCell className="text-red-500">42</TableCell>
                    <TableCell className="text-yellow-500">42</TableCell>
                    <TableCell className="text-green-500">42</TableCell>
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