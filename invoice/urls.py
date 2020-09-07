from django.urls import path
from . import views


urlpatterns = [
    path('invoiceupload/',views.invoice_upload,name='invoiceupload'),
    path('invoiceupdate/',views.invoice_update,name='invoiceupdate'),
    path('invoicecreate/',views.invoice_create,name='invoicecreate'),
    path('invoiceinfo/',views.invoice_info,name='invoiceinfo'),
]