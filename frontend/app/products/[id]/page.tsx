"use client";


import Head from "next/head";
import { usePathname } from "next/navigation";

import {
    Table,
    TableBody,
    TableCaption,
    TableCell,
    TableFooter,
    TableHead,
    TableHeader,
    TableRow,
  } from "@/components/ui/table";
import { use } from "react";
import useSWR from "swr";

export async function fetcher<JSON = any>(
  input: RequestInfo,
  init?: RequestInit
): Promise<JSON> {
  const res = await fetch(input, init)
  return res.json()
}


export default function Home() { 
    const id = usePathname().split("/")[2];
    const c = ["Bad microphone", "Comment1asdkajlkasjdkladjalsjdlasdjasldasda", "Good", "Okay"]



    return (
        <>
          <Head>
            <title> LauzHack 2023</title>
          </Head>
          <main className="flex justify-center min-h-screen flex-row w-full p-16">
            <Table>
              <TableHeader>
                <TableRow>
                {/* |issue| Sev level | # reviews | */}
                    <TableHead>Issue</TableHead>
                    <TableHead>Severity</TableHead>
                    <TableHead># Reviews</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {c.map((c, index) => (
                  index %2 == 0 ? <TableRow className="border-none" key={index}>
                    <TableCell>{c}</TableCell>
                    <TableCell>High</TableCell>
                    <TableCell>42</TableCell>
                  </TableRow > :
                    <TableRow key={index} className="bg-muted hover:bg-muted">
                        <TableCell colSpan={3}>{c}</TableCell>
                    </TableRow>
                ))}
              </TableBody>
            </Table>
          </main>  
        </>
        );
}