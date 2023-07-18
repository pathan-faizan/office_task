# # Requires Python 3.6 or higher due to f-strings

# # Import libraries
from tempfile import TemporaryDirectory
from pathlib import Path
import easyocr
from pdf2image import convert_from_path
from PIL import Image
import re
import PyPDF2
import sys



path_to_poppler_exe = Path(r"C:\Users\faiza\Downloads\Release-23.07.0-0\poppler-23.07.0\Library\bin")


inputPdf = input("Enter the name of the pdf file: ") 
outputPdf = input("Enter the name of the output pdf file: ")

PDF_file = Path(inputPdf)

image_file_list = []

pageCount = 0
lr_not_found = []
pdfFileObj = open(PDF_file, 'rb')   
pdfReader = PyPDF2.PdfReader(pdfFileObj)


print("Loading OCR model.................",end="\r")


with TemporaryDirectory() as tempdir:

    try:
        pdf_pages = convert_from_path(
                PDF_file, 500, poppler_path=path_to_poppler_exe
            )
    except:
        print("Error in loading pdf file or pdf path is not proper")    
        sys.exit(0)

    for page_enumeration, page in enumerate(pdf_pages, start=1):

        filename = f"{tempdir}\page_{page_enumeration:03}.jpg"
        print(f"Creating {filename}...")
        page.save(filename, "JPEG")
        image_file_list.append(filename)



    while pageCount < len(image_file_list):
        reader = easyocr.Reader(['en'])
        text = reader.readtext(Image.open(image_file_list[pageCount]), detail = 0)
        r = re.compile(r"\b[a-zA-Z]{2}[0-9]{8}\b")
        text = list(filter(r.match, text))
        if len(text)==0:
            if(pageCount%2!=0):
                lr_not_found.append((pageCount+1)/2)

            pageCount+=1
        else:
            if(pageCount%2==0):
                pdfWriter = PyPDF2.PdfWriter()
                pdfWriter.add_page(pdfReader.pages[pageCount])
                pdfWriter.add_page(pdfReader.pages[pageCount+1])
                text = text[0].upper()
                try:
                    newFile = open(f"{outputPdf}/{text}.pdf", 'wb')
                    pdfWriter.write(newFile)
                    newFile.close()
                except:
                    print("Error in saving pdf file or pdf output path is not proper")
                    sys.exit(0)    
            else:
                # remove all pages from pdfWriter
                pdfWriter = PyPDF2.PdfWriter()
                pdfWriter.add_page(pdfReader.pages[pageCount-1])
                pdfWriter.add_page(pdfReader.pages[pageCount])
                text = text[0].upper() 
                try:
                    newFile = open(f"{outputPdf}/{text}.pdf", 'wb')
                    pdfWriter.write(newFile)
                    newFile.close()  
                except:
                    print("Error in saving pdf file or pdf output path is not proper")
                    sys.exit(0)     
            pageCount+=2 
        

pdfFileObj.close()
if(len(lr_not_found)!=0):
    print("I did'nt get lr no. of these papers:", lr_not_found)
else:
    print("All lr no. found")    
print("Done................................",end="\r")



  

