// header component
// do not use links with a href attribute
// add name AWSFeedback on left mostside
import React from 'react';
import Link from 'next/link';

export default function Header() {
    return (
        <div className="flex flex-row items-center w-full h-16 bg-[#f2f2f2] rounded-b-3xl px-8 absolute">
            <Link href="/" className='text-xl text-[#FF9900] font-bold'>Elastic</Link>
            <Link href="/" className='text-xl text-[#131A22]'>Review</Link>
            <Link href="/" className='text-xl font-bold text-[#232F3E]'>Review</Link>
        </div>
    )
}