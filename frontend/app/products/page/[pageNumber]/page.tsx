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

export interface BadgeProps {
  color: string
  text: string
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
        <div className="flex items-left justify-center flex-col h-full w-full p-4 " >
          <div className="flex justify-center w-full h-24">
            <Input placeholder="Product name" className="w-[40%]"></Input>
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
                      <Button variant="ghost" onClick={request} disabled={c[index] != "Request"}>{
                        c[index] == "Active" ? "Active" :
                          c[index] == "Request" ? "Request" :
                            <CircularProgress isIndeterminate color='gray' size={30} />
                      }</Button>
                    </TableCell>
                    <TableCell className="py-[0.39rem]">{product}</TableCell>
                    <TableCell className="py-[0.39rem]">
                      <div className="flex flex-row">
                        <Badge color="#d13212" text="3"/>
                        <Badge color="#ebce38" text="12"/>
                        <Badge color="#1d8102" text="8"/>
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