# Project Writeup

## Approach & Assumptions

[Describe your overall approach to solving this problem. What was your thought process? What were the key challenges you identified?]

My first thought in solving this problem was the generalizability of the pipeline that I had to create. With the PDF's varied formatting and random assortment of products, I knew that my process would have to flexibly extract all relevant product information without limitation to the formatting. This led me to lean towards using the openai LLM as it has the ability to summarize and locate data under proper prompting. In arriving at this conclusion I developed my first version where I parsed the pdf file to get all the text using the PyMuPDF library and then prompted gpt to discern all the products and their manufacturers from that text. However, this relied on gpt to reason over large amounts of information all at once so it had a much harder time at correctly and accurately labling products and manufacturers. For this reason I implemented a two-step procedure to optimize gpt's effectiveness. First, I used the openai api to create a 2-3 sentence summary per page of the pdf. I then inputed this summarized version of the pdf into the openai api again to extract the product and manufacturers names. This created a more accurate output and allowed me to have more influence over the entire data extraction process.

## Limitations & Future Improvements

[If you had more time, what would you improve?]

Although my program does a good job at extracting the relevent products from the pdf it does have some areas of improvement. One of the major bugs that I have tried to mitigate are the cases where the submittor of the pdf is on pages but the true manufacturer was mentioned earlier and is not on the page. In these situations my program thinks that the contractor is the manufacturer. With more time I would continue to work on different ways to manipulate the data so that it is read under an umbrella of the manufacturer despite being on different pages. Another issue is the longer run time of the program because I use the api on a page by page basis when summarizing. To combat this there appears to be ways to parallelize calls which would enable the program to run much quicker and is something I would add with more time. The main issue that I have encountered is how important the prompting is. The smallest tweaks cause large changes so I would want to find a way that optimizes the prompt for all use cases.
