from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Invoice,InvoiceDetail 
import json
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view,parser_classes,permission_classes
from .extract_data import extract_text_from_pdf,convert_date
from rest_framework.permissions import AllowAny
from django.core.files.storage import FileSystemStorage
import os


#process uploaded invoice and extract date from it and save into database.
@api_view(['POST'])
@permission_classes([AllowAny])
@parser_classes([MultiPartParser, FormParser])
def invoice_upload(request):
	try:
		request_file = request.FILES['invoice'] if 'invoice' in request.FILES else None
		if request_file:
			fs = FileSystemStorage()
			file = fs.save(request_file.name, request_file)
			url = fs.url(file)
			fileurl = os.path.join( os.path.dirname( __file__ )).split('/')[:-1]
			fileurl =  "/".join(fileurl)+url
			invoice_data = extract_text_from_pdf(fileurl)
			print("d",invoice_data)
			invoice = Invoice()
			invoice.invoice = invoice_data['invoice']
			invoice.save()
			invoice_detail =  InvoiceDetail()
			invoice_detail.invoice = invoice
			invoice_detail.name = invoice_data['company']
			invoice_detail.email = invoice_data['email']
			invoice_detail.date = invoice_data['date']
			invoice_detail.address = invoice_data['address']
			invoice_detail.total = float(invoice_data['total'])
			invoice_detail.contact = invoice_data['contact']
			invoice_detail.save()
			return Response({"status_code":"200","info":invoice_data},status=status.HTTP_200_OK)
		else:
			return Response({"status_code":"401","message":"Invaild Date"},status=status.HTTP_400_BAD_REQUEST)
	except Exception as e:
		try:
			invoice.delete()
		except:
			pass
		return Response({"status_code":"400","message":str(e)},status=status.HTTP_400_BAD_REQUEST)

#update the existing invoice
@api_view(['PUT'])
@permission_classes([AllowAny])
def invoice_update(request):
	if request.method == 'PUT':
		try:
			invoice =  request.data['invoice']
			invoice =  Invoice.objects.get(invoice=invoice)
			invoice_detail =  InvoiceDetail.objects.get(invoice=invoice)
			try:
				name = request.data['name']
			except:
				name =  None
			try:
				email =  request.data['email']
			except:
				email = None
			try:
				contact = request.data['contact']
			except:
				contact = None
			try:
				date =  convert_date(request.data['date'])
			except:
				date = None
			try:
				total =  float(request.data['total'])
			except:
				total = None
			try:
				address = request.data['address']
			except:
				address = None
			if email:
				invoice_detail.email = email
			if contact:
				invoice_detail.contact = contact
			if date:
				invoice_detail.date =  date 
			if total:
				invoice_detail.total = total 
			if address:
				invoice_detail.address = address
			if name:
				invoice_detail.name =  name
			invoice_detail.save()
			return Response({"status_code":"200","info":"Invoice date updated sucessfully"},status=status.HTTP_200_OK)
		except Exception as e:
			return Response({"status_code":"400","message":str(e)},status=status.HTTP_400_BAD_REQUEST)

#create invoice manually from the user input.
@api_view(['POST'])
@permission_classes([AllowAny])
def invoice_create(request):
	if request.method == 'POST':
		try:
			invoice =  Invoice(invoice=request.data['invoice'])
			invoice.save()
			invoice_detail =  InvoiceDetail(invoice=invoice,name=request.data['name'],email=request.data['email'],contact=request.data['contact'],\
				date=convert_date(request.data['date']),address=request.data['address'],total=float(request.data['total']))
			invoice_detail.save()
			return Response({"status_code":"200","info":"Invoice created sucessfully"},status=status.HTTP_200_OK)
		except Exception as e:
			invoice.delete()
			return Response({"status_code":"400","message":str(e)},status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def invoice_info(request):
	try:
		invoice =  Invoice.objects.get(invoice=request.data['invoice'])
		invoice_detail = InvoiceDetail.objects.get(invoice=invoice)
		data = {
				"invoice":invoice.invoice,
				"name":invoice_detail.name,
				"email":invoice_detail.email,
				"contact":invoice_detail.contact,
				"date":invoice_detail.date,
				"total":invoice_detail.total
			}
		return Response({"status_code":"200","info":data},status=status.HTTP_200_OK)
	except Exception as e:
		return Response({"status_code":"400","message":str(e)},status=status.HTTP_400_BAD_REQUEST)


			

















