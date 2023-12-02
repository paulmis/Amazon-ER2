const GoogleImages = require('google-images');

const client = new GoogleImages(process.env.CSE_ID, process.env.API_KEY);

export const searchImage = async (query: string): Promise<string> => {
  const images = await client.search(query);
  const image = images[0];
  return image.url;
};
