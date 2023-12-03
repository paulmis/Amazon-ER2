import { Button } from '@/components/ui/button';
// get pageNumber from props

export const Pagination = ({ pageNumber }: { pageNumber: number }) => {

    const getRange = (pageNumber: number) => {
        const start = Math.floor(pageNumber / 5) * 5 + (pageNumber % 5 == 0 ? -4 : 1);
        const end = start + 5;
        return Array.from({ length: 5 }, (_, i) => start + i);
      }
      const pageNumberRange = getRange(pageNumber);

    const goToPage = (pageNumber: number) => {
        if (pageNumber < 1) return () => { window.location.href = `/404` }
        return () => { window.location.href = `/products/page/${pageNumber}` }
      }
    

    return (
        <div className="w-[20%]  h-10 flex flex-row">
            <Button variant="ghost" onClick={goToPage(pageNumber - 1)} className="">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5" />
                </svg>
            </Button>
            {pageNumberRange.map((p, index) => (
                p == pageNumber ?
                    <Button key={index} variant="ghost" className="bg-gray-200" >
                        {p}
                    </Button> :
                    <Button key={index} variant="ghost" onClick={goToPage(p)}>
                        {p}
                    </Button>
            ))}
            <Button variant="ghost" onClick={goToPage(pageNumber + 1)} className="p-none">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" />
                </svg>
            </Button>
        </div>
    )
}