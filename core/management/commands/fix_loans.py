from django.core.management.base import BaseCommand
from core.models import Loan
from datetime import date

class Command(BaseCommand):
    help = 'Logs all loans that are completed based on end_date'

    def handle(self, *args, **kwargs):
        today = date.today()
        completed_count = 0

        loans = Loan.objects.all()
        if not loans:
            self.stdout.write("No loans found in the system.")
            return

        for loan in loans:
            if loan.end_date < today:
                self.stdout.write(f"✅ Loan ID {loan.id} (Customer ID: {loan.customer.id}) ended on {loan.end_date}")
                completed_count += 1

        self.stdout.write(self.style.SUCCESS(f"\n🎯 Total completed loans (by end_date): {completed_count}"))
