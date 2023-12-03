// {
//     "example": {
//       "brand": "Apple",
//       "id": 1214,
//       "price": 33.0,
//       "product": "Apple iPhone 3GS 8GB Black Factory Unlocked / Not Jailbroken",
//       "rating": 1,
//       "review": "I paid 135 for this phone and when i received it i had to pay another hundred bucks to fix the screen and unlock it---------do not recomend",
//       "votes": 1
//     },
//     "item_count": 5,
//     "name": "screen damaged"
//   }

import { Product } from "./product";

// Issue schema has 
export default interface Issue {
    example: Product;
    item_count: number;
    name: string;
}