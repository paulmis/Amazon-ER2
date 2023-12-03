"use client";

import Review from "@/app/models/review";
import { Separator } from "@/components/ui/separator";
import { Table, TableBody, TableRow } from "@/components/ui/table";
import { redirect, usePathname } from "next/navigation";

// product/{product.id}/issue/{issue.id}
export default function ProductIssuePage() {
  const id = usePathname().split("/")[2];

  // check if id is a number
  // if not, redirect to 404
  if (isNaN(Number(id))) {
    redirect("/404");
  }

  const reviews: IssueCluster[] = [
    { id: 1, review: "Screen damaged", highlights: [0] },
    { id: 2, review: "This is a really bad microphone", highlights: [3, 4], rating: 3 }
  ]

  return (
    <>
      <main className="flex min-h-screen flex-col w-full p-16">
        <div className="flex  flex-col h-full w-full p-4 " >
          <div className="text-xl">Apple iPhone 3GS 8GB Black Factory Unlocked / Not Jailbroken</div>

          <div className="flex flex-row p-8 w-full">
            {
              <div className="flex flex-col w-full">
                {reviews.map((review, index) => (
                  <div key={index} className="flex flex-row">
                    {index + 1 + ". " + review.review}
                  </div>
                ))}
              </div>
            }


          </div>
        </div>
      </main>
    </>
  );
}