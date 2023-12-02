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




export default function Home() {

  const page = usePathname().split("/")[3];

  if (isNaN(Number(page))) { 
    redirect("/404");
  } else if (Number(page) < 1) {
    redirect("/404");
  }

  const c: string[] = ["Active", "Active", "Request", "Requesting"];
  
  // var { data, error, isLoading } = useSWR('api/products', fetcher);

  // if (isLoading) return <div>Loading...</div>
  // if (error) return <div>Error</div>

  // data = data as Product[];
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
          <div className="w-full">
            <Table>
              <TableHeader>
                <TableRow>
                  {/* |status| Product | # total sev | # high | # med | # low | */}

                  <TableHead>Status</TableHead>
                  <TableHead>Product</TableHead>
                  <TableHead># Severity </TableHead>
                  <TableHead># High</TableHead>
                  <TableHead># Medium</TableHead>
                  <TableHead># Low</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {c.map((c, index) => (
                  <TableRow key={index}>
                    <TableCell>
                      <Button variant="ghost" onClick={request} disabled={c != "Request"}>{
                        c == "Active" ? "Active" :
                          c == "Request" ? "Request" :
                            <CircularProgress isIndeterminate color='gray' size={30} />
                      }</Button>
                    </TableCell>
                    <TableCell>Product Name</TableCell>
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