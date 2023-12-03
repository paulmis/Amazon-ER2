"use client";

import { Comment } from "@/app/models/models";
import { redirect, usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import Link from "next/link";
// product/{product.id}/issue/{issue.id}
export default function ProductIssuePage() {
  const productName = usePathname().split("/")[2];
  const clusterName = usePathname().split("/")[4];
  const [loading, setLoading] = useState<boolean>(false);
  const [comments, setComments] = useState<Comment[]>([]);
  const [highlights, setHighlights] = useState<string[]>([]);
  const fetchCluster = async () => {
    setLoading(true);
    const res = await fetch(
      `http://localhost:5000/issues_for_cluster?product=${productName}&cluster_name=${clusterName}`
    );
    const json = (await res.json()) as Comment[];
    console.log(json);
    setComments(json);

    let highlights: string[] = [];
    // For all comments we do a post to /highlight with product_review and issue
    for (const comment of json) {
      const res = await fetch(`http://localhost:5000/highlight`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          product_review: comment.review,
          issue: decodeURIComponent(clusterName),
        }),
      });
      const json = await res.json();
      highlights.push(json.highlight);
    }
    setHighlights(highlights);
    setLoading(false);
  };

  useEffect(() => {
    fetchCluster();
  }, []);


  return (
    <>
      <main className="flex min-h-screen flex-col w-full p-8">
        <div className="flex justify-center">
          <div className="flex flex-row items-center w-[80%]">
            <Link
              color="rgb(26, 13, 171)"
              href={`/products/${productName}/issues`}
              className="text-xl py-2 w-[200px]"
              style={{ whiteSpace: "nowrap" }}
            >
              Product
            </Link>
            <div className="px-2">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                strokeWidth={1.5}
                stroke="currentColor"
                className="w-6 h-6"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M8.25 4.5l7.5 7.5-7.5 7.5"
                />
              </svg>
            </div>
            <div className="text-xl py-2">{decodeURIComponent(clusterName)}</div>
          </div>
        </div>
        <div className="flex flex-row h-full p-4 content-center justify-center">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead className="w-[60%]">Review</TableHead>
                <TableHead className="w-[20%]">Rating</TableHead>
                <TableHead className="w-[20%]">Number of likes</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {comments.map((comment, index) => {
                console.log(comment);
                return (
                  <TableRow key={index}>
                    <TableCell className="py-[0.39rem]">
                      {highlights[index] ? (
                        <span>
                          {comment.review
                            .split(highlights[index])
                            .map((part, idx, arr) =>
                              idx < arr.length - 1 ? (
                                <>
                                  <span>{part}</span>
                                  <span className="text-red-500">
                                    {highlights[index]}
                                  </span>
                                </>
                              ) : (
                                <span key={index}>{part}</span>
                              )
                            )}
                        </span>
                      ) : (
                        <span>{comment.review}</span>
                      )}
                    </TableCell>

                    <TableCell className="py-[0.39rem]">
                      <div className="flex flex-row items-center">
                        {[...Array(5)].map((_, index) =>
                          index < comment.rating ? (
                            <svg
                              key={index}
                              viewBox="0 0 24 24"
                              xmlns="http://www.w3.org/2000/svg"
                              className="w-6 h-6"
                            >
                              <path
                                d="M12 .587l3.668 7.568 8.332 1.151-6.064 5.828 1.48 8.279-7.416-3.967-7.417 3.967 1.481-8.279-6.064-5.828 8.332-1.151z"
                                className="fill-[#ff9900]"
                                transform="matrix(1, 0, 0, 1, 0, 8.881784197001252e-16)"
                              />
                              <path
                                d="M 11.995 5.19 L 14.33 10.007 L 19.635 10.739 L 15.774 14.449 L 16.716 19.719 L 11.995 17.195 L 7.274 19.72 L 8.216 14.45 L 4.355 10.74 L 9.66 10.007 L 11.995 5.19 Z M 11.995 0.604 L 8.327 8.172 L -0.005 9.323 L 6.059 15.151 L 4.579 23.43 L 11.995 19.463 L 19.411 23.429 L 17.931 15.15 L 23.995 9.323 L 15.663 8.173 L 11.995 0.604 Z"
                                className="fill-[#ff8200]"
                                transform="matrix(1, 0, 0, 1, 0, 8.881784197001252e-16)"
                              />
                            </svg>
                          ) : (
                            <svg
                              key={index}
                              viewBox="0 0 24 24"
                              xmlns="http://www.w3.org/2000/svg"
                              className="w-6 h-6"
                            >
                              <path
                                d="M12 5.173l2.335 4.817 5.305.732-3.861 3.71.942 5.27-4.721-2.524-4.721 2.525.942-5.27-3.861-3.71 5.305-.733 2.335-4.817zm0-4.586l-3.668 7.568-8.332 1.151 6.064 5.828-1.48 8.279 7.416-3.967 7.416 3.966-1.48-8.279 6.064-5.827-8.332-1.15-3.668-7.569z"
                                className="fill-[#ff8200]"
                                transform="matrix(1, 0, 0, 1, 0, 4.440892098500626e-16)"
                              />
                            </svg>
                          )
                        )}
                      </div>
                    </TableCell>
                    <TableCell className="py-[0.39rem]">
                      {comment.votes} Likes
                    </TableCell>
                  </TableRow>
                );
              })}
            </TableBody>
          </Table>
        </div>
      </main>
    </>
  );
}
