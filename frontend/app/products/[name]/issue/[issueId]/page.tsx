"use client";

import Review from "@/app/models/review";
import { redirect, usePathname } from "next/navigation";

// product/{product.id}/issue/{issue.id}
export default function ProductIssuePage() {
  const id = usePathname().split("/")[2];

  // check if id is a number
  // if not, redirect to 404
  if (isNaN(Number(id))) {
    redirect("/404");
  }

  const reviews: Review[] = [
    { id: 1, review: "Bad microphone", highlights: [0], rating: 5 },
    { id: 2, review: "This is a really bad microphone", highlights: [3, 4], rating: 3 }
  ]

  return (
    <>
      <main className="flex min-h-screen flex-col w-full p-16">
        <div className="flex  flex-col h-full w-full p-4 " >
          <div className="text-3xl"> Bad noise suppression </div>

          <div className="flex flex-row p-8 w-full">
            {
              <div className="flex flex-col w-full">
                {reviews.map((review, index) => (
                  <div key={index} className="flex flex-row">
                    {index + 1 + ". " + review.review}

                    {/* Rating stars */}
                    {[...Array(5)].map((_, index) => (
                      index < review.rating ?
                        <svg key={index} viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" className="w-6 h-6" style={{transform: "scale(0.7)"}}>
                          <path d="M12 .587l3.668 7.568 8.332 1.151-6.064 5.828 1.48 8.279-7.416-3.967-7.417 3.967 1.481-8.279-6.064-5.828 8.332-1.151z" className="fill-[#ff9900]" transform="matrix(1, 0, 0, 1, 0, 8.881784197001252e-16)" />
                          <path d="M 11.995 5.19 L 14.33 10.007 L 19.635 10.739 L 15.774 14.449 L 16.716 19.719 L 11.995 17.195 L 7.274 19.72 L 8.216 14.45 L 4.355 10.74 L 9.66 10.007 L 11.995 5.19 Z M 11.995 0.604 L 8.327 8.172 L -0.005 9.323 L 6.059 15.151 L 4.579 23.43 L 11.995 19.463 L 19.411 23.429 L 17.931 15.15 L 23.995 9.323 L 15.663 8.173 L 11.995 0.604 Z" className="fill-[#ff8200]" transform="matrix(1, 0, 0, 1, 0, 8.881784197001252e-16)" />
                        </svg> :
                        <svg key={index} viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" className="w-6 h-6">
                          <path d="M12 5.173l2.335 4.817 5.305.732-3.861 3.71.942 5.27-4.721-2.524-4.721 2.525.942-5.27-3.861-3.71 5.305-.733 2.335-4.817zm0-4.586l-3.668 7.568-8.332 1.151 6.064 5.828-1.48 8.279 7.416-3.967 7.416 3.966-1.48-8.279 6.064-5.827-8.332-1.15-3.668-7.569z" className="fill-[#ff8200]" transform="matrix(1, 0, 0, 1, 0, 4.440892098500626e-16)" />
                        </svg>
                    ))}
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