"use client";

import { redirect, useParams, usePathname } from "next/navigation";
import { Badge } from "../../page/[pageNumber]/page";
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { Link } from "@chakra-ui/react";
import { useEffect, useState } from "react";
import { IssueCluster } from "@/app/models/models";
import WordCloudUI from "@/components/wordCloud";

function capitalizeFirstLetter(string: string) {
  return string.charAt(0).toUpperCase() + string.slice(1);
}

// product/{product.id}/issue/{issue.id}
export function ProductIssuePage({ name }: { name: string }) {
  const [loading, setLoading] = useState<boolean>(false)
  const [clusters, setClusters] = useState<IssueCluster[]>([])

  const id = usePathname().split("/")[2]

  const fetchCluster = async (product: string) => {
    setLoading(true)
    const res = await fetch(`http://localhost:5000/issues?product=${encodeURIComponent(product)}`)
    const json = await res.json() as IssueCluster[]
    setClusters(json)
    setLoading(false)
  }

  const data = [
    { text: 'Hey', value: 1000 },
    { text: 'lol', value: 200 },
    { text: 'first impression', value: 800 },
    { text: 'very cool', value: 1000000 },
    { text: 'duck', value: 10 },
  ];




  useEffect(() => {
    fetchCluster(name)
  }, [])

  return (
    <>
      <main className="flex min-h-screen flex-col w-full p-8">
        <div className="flex justify-center">
          <div className="flex flex-row items-center w-[80%]">
            <Link color='rgb(26, 13, 171)' href="/products/page/1" className="text-xl py-2 w-[200px]" style={{ whiteSpace: "nowrap" }}>All products</Link>
            <div className="px-2">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6">
                <path strokeLinecap="round" strokeLinejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" />
              </svg>
            </div>
            <div className="text-xl py-2">{name}</div>
          </div>
        </div>
        <div className="flex flex-row h-full p-4">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead className="w-[5%]">Issue</TableHead>
                <TableHead className="w-[10%]">Details</TableHead>
                <TableHead className="w-[1%]">Reviews</TableHead>
                <TableHead className="w-[20%]">Example review</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {clusters.map((cluster, index) => {
                console.log(cluster)
                return (
                  <TableRow key={index}>
                    <TableCell className="py-[0.39rem]">
                      {capitalizeFirstLetter(cluster.name)}
                    </TableCell>
                    <TableCell className="py-[0.39rem]">
                      {[...new Set(cluster.issues.map(issue => issue.issue))].join(", ")}
                    </TableCell>
                    <TableCell className="py-[0.39rem]">
                      {cluster.item_count}
                    </TableCell>
                    <TableCell className="py-[0.39rem]">
                      {
                        cluster.example.review.length > 150 ?
                          cluster.example.review.substring(0, 150) + "..." :
                          cluster.example.review
                      }
                    </TableCell>
                  </TableRow>
                )
              })}
            </TableBody>
          </Table>
          <div className="w-[50%]">
           <WordCloudUI data = { clusters.map(cluster => ({ text: cluster.name, value: cluster.item_count * 3 }))}></WordCloudUI>

          </div>
        </div>
      </main>
    </>
  );
}

export default function GetProductIssuePage() {
  const x = useParams().name as String;
  if (typeof x !== "string") redirect("/404");
  const name = decodeURIComponent(x);

  return ProductIssuePage({ name: name })
}