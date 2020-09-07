from django.db import models

# Create your models here.
class Invoice(models.Model):
	invoice =  models.CharField(max_length=30,unique=True)

class InvoiceDetail(models.Model):
	invoice = models.ForeignKey(Invoice,on_delete=models.CASCADE)
	name = models.CharField(max_length=30)
	address = models.CharField(max_length=100)
	date = models.DateField()
	email = models.CharField(max_length=30)
	contact = models.CharField(max_length=15)
	total = models.DecimalField(default=0.0,max_digits=10, decimal_places=2)

	def __str__(self):
		return self.name



