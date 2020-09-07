# Import libraries 
from PIL import Image 
import pytesseract 
import sys 
from pdf2image import convert_from_path
from nltk.tokenize import word_tokenize
import os 
import re
from datetime import datetime

#convert date format for saving
def convert_date(date):
	try:
		new_date = datetime.strptime(date, '%m/%d/%Y').strftime('%Y-%m-%d')
	except:
		new_date = datetime.strptime(date, '%d/%m/%Y').strftime('%Y-%m-%d')
	return new_date

#convert pdf into image and extract text from the image using tessract and return invoice information in dictonary
def extract_text_from_pdf(PDF_file):
	pages = convert_from_path(PDF_file, 500) 
	image_counter = 1
	for page in pages: 
		filename = "page_"+str(image_counter)+".jpg"
		page.save(filename, 'JPEG') 
		image_counter = image_counter + 1
	filelimit = image_counter-1
	for i in range(1, filelimit + 1): 
		filename = "page_"+str(i)+".jpg"
		text = str(((pytesseract.image_to_string(Image.open(filename))))) 
		invoice_info = {} 
		invoice_text = text.replace('\n\n','\n').split('\n')
		# invoice_text = text.split('\n')
		print("i",invoice_text)
		invoice_text_length =  len(invoice_text)
		for word in range(invoice_text_length):
			if invoice_text[word] == 'Bill to:':
				try:
					invoice_info['company'] = invoice_text[word+1]
					invoice_info['contact'] = invoice_text[word+2] 
					invoice_info['email'] = invoice_text[word+3]
					count = 5
					while invoice_text[word+count]!='' and count<7:
						if 'address' not in invoice_info:
							invoice_info['address'] =  invoice_text[word+count]
						else:
							invoice_info['address'] +=  invoice_text[word+count]
						count += 1
				except Exception as e:
					print(str(e))

		#replace space between numbers
		amount = re.sub('(?<=\d) (?=\d)', '',text)
		amounts = re.findall(r'(\d+\.\d{1,2})',amount)
		invoice_info['total'] = amounts[-1]
		#get the invoice from the template
		inv = list(filter((lambda x:'# INV' in x),invoice_text))
		invoice_info['invoice'] = inv[0].replace('#','').replace(' ','')
		invoice_info['date'] = convert_date(re.findall(r"\d{1,2}/\d{1,2}/\d{4}",text)[0])
	return invoice_info

if __name__ == '__main__':
	extract_text_from_pdf(pdf)





