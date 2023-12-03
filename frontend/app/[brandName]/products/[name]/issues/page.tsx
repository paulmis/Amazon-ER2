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
import { Image, Link } from "@chakra-ui/react";
import { useEffect, useState } from "react";
import { IssueCluster } from "@/app/models/models";
import WordCloudUI from "@/components/wordCloud";
import Header from "@/components/ui/header";
import SubHeader from "@/components/ui/subheader";

function capitalizeFirstLetter(string: string) {
  return string.charAt(0).toUpperCase() + string.slice(1);
}

// product/{product.id}/issue/{issue.id}
export default function ProductIssuePage() {
  const [loading, setLoading] = useState<boolean>(false)
  const [clusters, setClusters] = useState<IssueCluster[]>([])
  var brandParam = useParams().brandName , nameParam = useParams().name;
  if (typeof brandParam !== "string" || typeof nameParam !== "string") redirect("/404");
  const brandName: string = decodeURIComponent(brandParam as string);
  const name: string = decodeURIComponent(nameParam as string);

  const fetchCluster = async (product: string) => {
    setLoading(true)
    const res = await fetch(`http://localhost:5000/issues?product=${encodeURIComponent(product)}`)
    const json = await res.json() as IssueCluster[]
    setClusters(json)
    setLoading(false)
  }

  console.log(brandName, name);


  useEffect(() => {
    fetchCluster(name)
  }, []);

  const totalReviews = clusters.reduce((acc, cluster) => acc + cluster.item_count, 0)

  return (
    <>
      <Image className="absolute z-10 top-[100px] right-[300px]" height={200} width={200} src={`http://localhost:5000/image?product=${encodeURIComponent(name)}`}></Image>
      
      <Header/>
      <main className="flex min-h-screen flex-col w-full p-8 pt-20">
        <div className="flex items-left justify-center flex-col h-full w-full p-4 ">
          <SubHeader url={`/${encodeURIComponent(brandName)}/products/page/1`} goBack="All Products" name = {name} size="xl"></SubHeader>
          {/* <div className="flex justify-center">
            <div className="flex flex-row items-center w-[80%] pb-10">
              <div className="px-2">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5" />
                </svg>
              </div>
            </div>
          </div> */}
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
                    <Link href={`/${brandName}/products/${encodeURIComponent(name)}/issue/${encodeURIComponent(cluster.name)}`}>
                      {capitalizeFirstLetter(cluster.name)}
                    </Link>
                    </TableCell>
                    <TableCell className="py-[0.39rem]">
                      {[...new Set(cluster.issues.map(issue => issue.issue))].join(", ")}
                    </TableCell>
                    <TableCell className="">
                      {cluster.item_count}&#160;&#160;&#160;{((cluster.item_count / totalReviews) * 100).toFixed(0)}%
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
          <div className="flex w-[80%] flex-col translate-y-[50px]">
            <WordCloudUI data = { clusters.map(cluster => ({ text: cluster.name, value: cluster.item_count * 3 }))}></WordCloudUI>
          </div>
        </div>
      </main>

    </>
  );
}
