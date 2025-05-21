import os
import io
import pandas as pd
import sys
import parser
import pandas as pd
from pandas import DataFrame
from typing import List
from dotenv import load_dotenv
from openai import OpenAI

# @function page_summary
# @desc Summarizes the extracted text from each page of the PDF.
# @param pdf List[str] - A list of text strings, one for each page of the PDF.
# @returnType str
# @return A concatenated string of page summaries.
def page_summary(pdf: List[str]) -> str:
    
    dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    load_dotenv(dotenv_path)

    # Create OpenAI client
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    #Variable to track page summaries
    doc_summary = ''

    for i, page_text in enumerate(pdf):
        prompt = f"""
You are a technical document summarizer.

Below is the text extracted from **page {i+1}** of a construction submittal PDF.

--- PAGE {i+1} CONTENT START ---
{page_text}
--- PAGE {i+1} CONTENT END ---

Your task:
- Summarize this page in 2–3 sentences.
- **Emphasize** any product names, model numbers, and product categories.
- **Highlight** the manufacturer company, if mentioned.
- If a company is mentioned in the Submittal Data it CANNOT be the manufacturer. DO NOT MENTION THIS COMPANY.
- If the supplier is not explicitly mentioned on a page refer back to when supplier was explicitly stated and use that.
- Ignore irrelevant project metadata or boilerplate text.

Respond only with the summary. Do not include headers or formatting.
"""

        # Prompt GPT
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        # Get text content
        content = response.choices[0].message.content.strip()
        doc_summary += f"\nPAGE {i+1}:" + content

    return doc_summary

# @function extracted_products
# @desc Extracts structured product and manufacturer data from summarized pages.
# @param summary str - A multi-page summary string generated from the PDF pages.
# @returnType DataFrame
# @return A DataFrame containing product_name, manufacturer, and pages.
def extracted_products(summary: str) -> DataFrame:

    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    prompt = f"""
You are a data extractor for construction product submittals.

Below is a multi-page summary of a technical submittal document. Each page may describe one or more products, including specifications, model numbers, and manufacturers.

Your task is to:
1. Identify each unique product.
2. Return a **clean, generalized name** for each product including model numbers (grouping similar variants).
3. Assign the most accurate manufacturer name available. Normalize manufacturer names to the most standard form. 
*If manufacturer UNKNOWN use most PREVIOUSLY used manufacturer.
- If a company is mentioned in the Submittal Data it CANNOT be the manufacturer. DO NOT MENTION THIS COMPANY.
4. Identify a **clean, generalized name** manufacturer associated to the product.
5. Identify and MERGE ALL PRODUCTS that are similarly related under a **clean, generalized name** DO NOT REPEAT
6. Find all relevant pages for the the product.
7. Respond ONLY in valid CSV format.

Output Format:
- Columns: `product_name,manufacturer,pages` 
- Enclose any product and manufacturer names that contain commas in **double quotes**
- Do not include explanation, headers, markdown, or commentary

Example Format:
"product_name","manufacturer","[pages]"

--- BEGIN SUMMARIES ---
{summary}
--- END SUMMARIES ---
"""

    # Prompt GPT
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    content = response.choices[0].message.content.strip()

    # Strip markdown formatting if GPT wrapped output in code block
    if content.startswith("```"):
        content = content.strip("`").strip("json").strip()

    try:
        # Clean up GPT formatting
        if content.startswith("```"):
            content = content.strip("`").strip("csv").strip()

        # Parse CSV from string into DataFrame
        df = pd.read_csv(io.StringIO(content))
        return df
    except Exception as e:
        print("Failed to parse GPT CSV output.", content)
        print(content)
        raise e

# Test Methods
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python extractor.py path/to/pdf")
        sys.exit(1)

    pdf_path = sys.argv[1]
    pages = parser.extract_text_from_pdf(pdf_path)

    summary = page_summary(pages)
    extracted_data = extracted_products(summary)
    extracted_data.to_csv("products.csv", index=False)
    print(summary)