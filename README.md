# 💳 AI-Driven Credit Approval System

This is a full-stack Django-based web application designed to simulate a commercial loan underwriting platform. It allows customer onboarding, credit eligibility checks, loan creation, payment tracking, and credit score calculation. Dockerized and ready for deployment.

---

## 🚀 Features

- ✅ Customer Registration via Excel or API
- ✅ Credit Eligibility Checker
- ✅ Loan Creation & Management
- ✅ Loan Payment Tracking
- ✅ Credit Score Generation
- ✅ Admin Commands for Loan Fixing
- ✅ Fully Dockerized for Easy Deployment

---

## 📁 Project Structure

credit_approval_system/
│
├── core/ # Django app
│ ├── models.py # DB models
│ ├── views.py # API logic
│ ├── urls.py # API routes
│ └── management/ # Custom admin commands
│
├── requirements.txt # Python dependencies
├── Dockerfile # Docker config
├── docker-compose.yml # Docker multi-container config
└── README.md # You're here


---

## 🧪 API Endpoints

| Endpoint | Method | Description |
|---------|--------|-------------|
| `/register/` | POST | Register a customer |
| `/check-eligibility/` | POST | Check loan eligibility |
| `/create-loan/` | POST | Create a new loan |
| `/view-loans/<customer_id>/` | GET | View customer's loans |
| `/make-payment/` | POST | Make a payment |
| `/credit-score/<customer_id>/` | GET | Generate credit score |

---

## 📊 Sample Payloads

### 🔹 Register Customer

```json
{
  "first_name": "John",
  "last_name": "Doe",
  "age": 30,
  "phone_number": "9876543210",
  "monthly_salary": 50000,
  "approved_limit": 150000,
  "current_debt": 0
}
🐳 Docker Setup
🔧 Build & Run:
docker compose up --build
🛠 Run Migrations:
docker exec -it credit_approval_system-web-1 python manage.py migrate
📥 Import Customers from Excel:
docker exec -it credit_approval_system-web-1 python manage.py import_excel
🧹 Fix Completed Loans:
docker exec -it credit_approval_system-web-1 python manage.py fix_loans
🌐 Access Locally
http://localhost:8000/


🧠 Tech Stack
Python 3.10

Django 5.2

Django REST Framework

PostgreSQL

Docker

Pandas & OpenPyXL (for Excel import)

📌 Author
Deborshi Ganguly
👨‍💻 Built with ❤️ by a passionate developer
📫 Reach me on GitHub

🧪 License
This project is licensed under the MIT License.


---

Let me know if you want me to:

- Add **badges** (build passing, Dockerized, etc.)
- Create a **GitHub repo** for you
- Make it more professional or beginner-friendly
- Guide you in pushing this to GitHub

Ready to help you finish this like a pro 💪




