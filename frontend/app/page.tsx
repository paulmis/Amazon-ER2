import { Button } from "@/components/ui/button";
import Link  from "next/link";

export default function Home() {
  return (
    <>
      <div className = "flex min-h-screen flex-col justify-center items-center">
          <Link href="/products/page/1"> Products </Link>
          <Link href="/items"> Items </Link>

      </div>
    </>
  );
}