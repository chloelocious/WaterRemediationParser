import PyPDF2
import os

# path to the directory containing PDF files
pdf_dir = '/home/ssarrouf/Documents/webscrape/to_date_papers/spr_pdf_files'

# path to the directory to save the TXT files
txt_dir = '/home/ssarrouf/Documents/webscrape/to_date_papers/spr_txt_files'

for pdf_file in os.listdir(pdf_dir):
    if pdf_file.endswith('.pdf'):
        with open(os.path.join(pdf_dir, pdf_file), 'rb') as pdf:
            try:
                pdf_reader = PyPDF2.PdfReader(pdf)
                pdf_content = ''
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    pdf_content += page.extract_text()
                txt_file = os.path.splitext(pdf_file)[0] + '.txt'
                with open(os.path.join(txt_dir, txt_file), 'w') as txt:
                    txt.write(pdf_content)
            except PyPDF2.errors.PdfReadError:
                print(f"Error reading {pdf_file}: EOF marker not found")