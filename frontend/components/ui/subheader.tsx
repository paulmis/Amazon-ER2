import Link from "next/link";

export default function SubHeader({ url, goBack, name, size }: { url: string, goBack: string, name: string, size: string }) {
  const style = "text-" + size + " py-2 text-[#00000] font-bold"
  return (
    <div className="flex flex-row items-center pb-10 w-[70%]">
      <Link href={url} className = "flex flex-row items-center">
        <div className="px-2 ">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="#146eb4" className="w-6 h-6">
            <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5" />
          </svg>
        </div>
        <div className="text-xl py-2 pr-10 text-[#146eb4] flex-wrap" style={{ whiteSpace: "nowrap" }}>{goBack}</div></Link>
      <p className={style}>{name}</p>
    </div>
  );
}