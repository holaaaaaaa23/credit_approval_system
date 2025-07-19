




# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from .models import Customer
# import json
# import math

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
#                 current_debt=data['current_debt']
#             )

#             return JsonResponse({
#                 'customer_id': customer.id,
#                 'message': 'Customer registered successfully'
#             })

#         except KeyError as e:
#             return JsonResponse({'error': f'Missing key: {str(e)}'}, status=400)
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)

#     return JsonResponse({'error': 'Only POST method allowed'}, status=405)


# @csrf_exempt
# def check_eligibility(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             customer = Customer.objects.get(id=data['customer_id'])

#             loan_amount = data['loan_amount']
#             interest_rate = data['interest_rate']
#             tenure = data['tenure']

#             # EMI Calculation
#             r = interest_rate / 12 / 100
#             n = tenure
#             emi = loan_amount * r * (1 + r)**n / ((1 + r)**n - 1)
#             emi = round(emi, 2)

#             total_obligation = customer.current_debt + emi
#             foir = total_obligation / customer.monthly_salary

#             if foir < 0.5:
#                 approved = True
#                 reason = "Eligible as per FOIR"
#             else:
#                 approved = False
#                 reason = "FOIR too high"

#             return JsonResponse({
#                 'customer_id': customer.id,
#                 'loan_amount': loan_amount,
#                 'interest_rate': interest_rate,
#                 'tenure': tenure,
#                 'monthly_installment': emi,
#                 'approval': approved,
#                 'approval_reason': reason
#             })

#         except Customer.DoesNotExist:
#             return JsonResponse({'error': 'Customer not found'}, status=404)
#         except KeyError as e:
#             return JsonResponse({'error': f'Missing key: {str(e)}'}, status=400)
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)

#     return JsonResponse({'error': 'Only POST method allowed'}, status=405)



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from core.models import Customer, Loan
import json
import math
import datetime


@csrf_exempt
def register_customer(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        required_fields = ['first_name', 'last_name', 'age', 'phone_number', 'monthly_salary', 'approved_limit', 'current_debt']
        for field in required_fields:
            if field not in data:
                return JsonResponse({'error': f"Missing key: '{field}'"}, status=400)

        customer = Customer.objects.create(
            first_name=data['first_name'],
            last_name=data['last_name'],
            age=data['age'],
            phone_number=data['phone_number'],
            monthly_salary=data['monthly_salary'],
            approved_limit=data['approved_limit'],
            current_debt=data['current_debt']
        )

        return JsonResponse({'customer_id': customer.id, 'message': 'Customer registered successfully'})

    return JsonResponse({'error': 'Only POST method allowed'}, status=400)


@csrf_exempt
def check_eligibility(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        try:
            customer = Customer.objects.get(id=data['customer_id'])
        except Customer.DoesNotExist:
            return JsonResponse({'error': 'Customer not found'}, status=404)

        loan_amount = data['loan_amount']
        interest_rate = data['interest_rate']
        tenure = data['tenure']

        r = interest_rate / 12 / 100
        n = tenure
        emi = loan_amount * r * (1 + r)**n / ((1 + r)**n - 1)
        emi = round(emi, 2)

        total_obligation = customer.current_debt + emi
        foir = total_obligation / customer.monthly_salary

        if foir < 0.5:
            approved = True
            reason = "Eligible as per FOIR"
        else:
            approved = False
            reason = "FOIR too high"

        return JsonResponse({
            'customer_id': customer.id,
            'loan_amount': loan_amount,
            'interest_rate': interest_rate,
            'tenure': tenure,
            'monthly_installment': emi,
            'approval': approved,
            'approval_reason': reason
        })

    return JsonResponse({'error': 'Only POST allowed'}, status=400)


@csrf_exempt
def create_loan(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        try:
            customer = Customer.objects.get(id=data['customer_id'])
        except Customer.DoesNotExist:
            
            return JsonResponse({'error': 'Customer not found'}, status=404)

        loan_amount = data['loan_amount']
        interest_rate = data['interest_rate']
        tenure = data['tenure']

        r = interest_rate / 12 / 100
        n = tenure
        emi = loan_amount * r * (1 + r)**n / ((1 + r)**n - 1)
        emi = round(emi, 2)

        total_obligation = customer.current_debt + emi
        foir = total_obligation / customer.monthly_salary

        if foir >= 0.5:
            return JsonResponse({
                'approval': False,
                'reason': 'FOIR too high, loan cannot be approved.'
            }, status=400)

        start_date = datetime.date.today()
        end_date = start_date + datetime.timedelta(days=30 * tenure)

        loan = Loan.objects.create(
            customer=customer,
            loan_amount=loan_amount,
            interest_rate=interest_rate,
            tenure=tenure,
            monthly_installment=emi,
            start_date=start_date,
            end_date=end_date,
            emis_paid_on_time=0
        )

        customer.current_debt += emi
        customer.save()

        return JsonResponse({
            'loan_id': loan.id,
            'message': 'Loan created successfully',
            'monthly_installment': emi
        })

    return JsonResponse({'error': 'Only POST allowed'}, status=400)
from django.views.decorators.http import require_GET

@require_GET
def get_all_customers(request):
    customers = Customer.objects.all().values()
    return JsonResponse(list(customers), safe=False)

@require_GET
def view_loans_by_customer(request, customer_id):
    try:
        loans = Loan.objects.filter(customer_id=customer_id).values()
        return JsonResponse(list(loans), safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
@csrf_exempt
def make_payment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            loan_id = data.get('loan_id')
            amount_paid = data.get('amount_paid')
            payment_date = data.get('payment_date')  # Optional for now

            # Get loan
            loan = Loan.objects.get(id=loan_id)
            customer = loan.customer

            # Update EMIs paid
            loan.emis_paid_on_time += 1
            loan.save()

            # Update customer's current debt
            customer.current_debt -= amount_paid
            customer.save()

            return JsonResponse({
                'loan_id': loan.id,
                'message': 'Payment processed successfully',
                'emis_paid_on_time': loan.emis_paid_on_time,
                'current_debt': customer.current_debt
            })

        except Loan.DoesNotExist:
            return JsonResponse({'error': 'Loan not found'}, status=404)
        except KeyError as e:
            return JsonResponse({'error': f'Missing key: {str(e)}'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Only POST method allowed'}, status=405)
@csrf_exempt
def credit_score(request, customer_id):
    if request.method == 'GET':
        try:
            customer = Customer.objects.get(id=customer_id)
            loans = customer.loans.all()

            if not loans:
                return JsonResponse({'credit_score': 0, 'message': 'No loans found'})

            total_paid = sum([loan.emis_paid_on_time for loan in loans])
            total_loans = sum([loan.tenure for loan in loans])

            score = round((total_paid / total_loans) * 900) if total_loans > 0 else 0

            return JsonResponse({'customer_id': customer.id, 'credit_score': score})

        except Customer.DoesNotExist:
            return JsonResponse({'error': 'Customer not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


            
@csrf_exempt
def view_loans(request, customer_id):
    if request.method == 'GET':
        try:
            customer = Customer.objects.get(id=customer_id)
            loans = customer.loans.all()

            loan_data = [{
                'loan_id': loan.id,
                'loan_amount': loan.loan_amount,
                'interest_rate': loan.interest_rate,
                'tenure': loan.tenure,
                'monthly_installment': loan.monthly_installment,
                'start_date': loan.start_date,
                'end_date': loan.end_date,
                'emis_paid_on_time': loan.emis_paid_on_time
            } for loan in loans]

            return JsonResponse({'customer_id': customer_id, 'loans': loan_data})

        except Customer.DoesNotExist:
            return JsonResponse({'error': 'Customer not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Only GET allowed'}, status=405)



