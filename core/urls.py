from django.urls import path
from .views import register_customer, check_eligibility, create_loan, view_loans, make_payment, credit_score

urlpatterns = [
    path('register/', register_customer),
    path('check-eligibility/', check_eligibility),
    path('create-loan/', create_loan),
    path('view-loans/<int:customer_id>/', view_loans),
    path('make-payment/', make_payment),
    path('credit-score/<int:customer_id>/', credit_score),
]

