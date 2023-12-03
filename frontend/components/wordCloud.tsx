import WordCloud from "react-d3-cloud";

export default function WordCloudUI({data} : {data: any}) {
    return (
        <WordCloud data = {data} width={100} height={100} rotate={() => (~~(Math.random() * 6) - 3) * 15}>
            
        </WordCloud>
    );
}