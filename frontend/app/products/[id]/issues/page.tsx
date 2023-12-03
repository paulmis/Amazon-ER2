"use client";

import { Comment, IssueCluster } from "@/app/models/models";
import { redirect, usePathname } from "next/navigation";
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
import { Button } from "@/components/ui/button";

function capitalizeFirstLetter(string: string) {
  return string.charAt(0).toUpperCase() + string.slice(1);
}

// product/{product.id}/issue/{issue.id}
export default function ProductIssuePage() {
  const id = usePathname().split("/")[2];

  // check if id is a number
  // if not, redirect to 404
  if (isNaN(Number(id))) {
    redirect("/404");
  }

  const clusters: IssueCluster[] = [
    {
      example: {
        brand: "Apple",
        id: 1214,
        price: 33.0,
        product: "Apple iPhone 3GS 8GB Black Factory Unlocked / Not Jailbroken",
        rating: 1,
        review: "I paid 135 for this phone and when i received it i had to pay another hundred bucks to fix the screen and unlock it---------do not recomend",
        votes: 1
      } as Comment,
      issues: ["broken screen, faulty LCD, bad screen"],
      item_count: 5,
      name: "screen damaged"
    }
  ]

  return (
    <>
      <main className="flex min-h-screen flex-col w-full p-16">
          <div className="flex justify-center">
            <div className="flex flex-col">
              <div className="text-xl py-2">Apple iPhone 3GS 8GB Black Factory Unlocked / Not Jailbroken</div>
            </div>
          </div>
        <div className="flex flex-col h-full w-[65%] p-4">
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
            {clusters.map((cluster, index) => (
              <TableRow key={index}>
                <TableCell className="py-[0.39rem]">
                  {capitalizeFirstLetter(cluster.name)}
                </TableCell>
                <TableCell className="py-[0.39rem]">
                  {cluster.issues}
                </TableCell>
                <TableCell className="py-[0.39rem]">
                  {cluster.item_count}
                </TableCell>
                <TableCell className="py-[0.39rem]">
                  {cluster.example.review}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
        </div>
      </main>
    </>
  );
}