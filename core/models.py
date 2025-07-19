# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from core.models import Customer
# import json

# @csrf_exempt
# def register_customer(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)

#             customer = Customer.objects.create(
#                 first_name=data['first_name'],
#                 last_name=data['last_name'],
#                 age=data['age'],
#                 phone_number=data['phone_number'],
#                 monthly_salary=data['monthly_salary'],
#                 approved_limit=data['approved_limit'],
#                 current_debt=data.get('current_debt', 0.0)
#             )

#             return JsonResponse({
#                 'message': 'Customer registered successfully',
#                 'customer_id': customer.id
#             }, status=201)

#         except KeyError as e:
#             return JsonResponse({'error': f'Missing field: {str(e)}'}, status=400)
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)

#     return JsonResponse({'error': 'Only POST allowed'}, status=405)
from django.db import models

class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField()
    phone_number = models.CharField(max_length=15)
    monthly_salary = models.IntegerField()
    approved_limit = models.IntegerField()
    current_debt = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Loan(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="loans")
    loan_amount = models.FloatField()
    interest_rate = models.FloatField()
    tenure = models.IntegerField()
    monthly_installment = models.FloatField()
    start_date = models.DateField()
    end_date = models.DateField()
    emis_paid_on_time = models.IntegerField()

    def __str__(self):
        return f"Loan {self.id} for {self.customer}"

