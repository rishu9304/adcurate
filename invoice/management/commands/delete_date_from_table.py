from django.core.management.base import BaseCommand, CommandError
from invoice.models import Invoice


class Command(BaseCommand):
	help = 'Closes the specified poll for voting'
	def handle(self, *args, **options):
		delete_invoices()

def delete_invoices():
	try:
		invoice =  Invoice.objects.all()
		for ins in invoice:
			data =  Invoice.objects.get(id=ins.id)
			data.delete()
		print("All Invoice deleted")
	except Exception as e:
		print(str(e)) 