import WordCloud from "react-d3-cloud";

export default function WordCloudUI({data} : {data: any}) {
    return (
        <WordCloud data = {data} width = {100} height = {100} font="serif" rotate={0}>
            
        </WordCloud>
    );
}