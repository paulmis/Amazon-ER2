// header component
// do not use links with a href attribute
// add name AWSFeedback on left mostside
import React from 'react';
import Link from 'next/link';

export default function Header() {
    return (
        <div className="flex flex-row items-center w-full h-16 bg-gray-400 rounded-b-3xl px-8 absolute">
            <Link href="/" className='text-xl text-white font-bold'>AWS</Link>
            <Link href="/" className='text-xl text-white'>Feedback</Link>
        </div>
    )
}