import sys
import os
import extractor
import parser

# Check valid args
if len(sys.argv) != 3:
    print("Usage: python parser.py path/to/pdf file.csv")
    sys.exit(1)
pdf_path = sys.argv[1]
csv_file = sys.argv[2]

# Parse PDF, Summarize Pages, and define products in a CSV
pages = parser.extract_text_from_pdf(pdf_path)
pages_summary = extractor.page_summary(pages)
df = extractor.extracted_products(pages_summary)

# Ensure folder exists
output_folder = os.path.join("output")
os.makedirs(output_folder, exist_ok=True)
csv_path = os.path.join(output_folder, csv_file)
df.to_csv(csv_path, index=False)
print("Successfully uploaded to csv file " + csv_file)