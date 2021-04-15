# https://www.youtube.com/watch?v=FQH_m-GEkdI
import csv,json,zipfile
import requests
import PyPDF2
import fitz
import sys
import re

def getpdfdetails(fname):
    doc = fitz.open(fname)  # open document
    #out = open(fname + ".txt", "wb")  # open text output
    for page in doc:  # iterate the document pages
        text = page.get_text('text')  # get plain text (is in UTF-8)
        lines=text.split('\n')
        for i,line in enumerate(lines):
            #print(line)
            m = re.match("DESCRIPTION", line)
            if m:
                print(line)
                print("Stock Symbol",lines[i+2])
                print("Purchase or Sell",lines[i+3])
                print("Purchase Date",lines[i+4])


zip_file_url="https://disclosures-clerk.house.gov/public_disc/financial-pdfs/2021FD.ZIP"
pdf_file_url="https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/2021/"
r=requests.get(zip_file_url)
zipfile_name = '2021.zip'


with open(zipfile_name, 'wb') as f:
    f.write(r.content)


with zipfile.ZipFile(zipfile_name) as z:
    z.extractall('.')


with open('2021FD.txt') as f:
    for line in csv.reader(f,delimiter='\t'):
        #print(line[1])
        if line[1] == 'Pelosi':
            date = line[7]
            doc_id = line[8]
            #print(date,doc_id)
            r = requests.get(f"{pdf_file_url}{doc_id}.pdf")
            outputpdf=f"{doc_id}.pdf"
            with open(outputpdf,'wb') as pdf_file:
                pdf_file.write(r.content)
                #getpdfdetails(outputpdf) #commented out this will give granular details of each pdf.
