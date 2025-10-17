# 🧮 Credit Scoring API

The **Credit Scoring API** evaluates borrower profiles and returns a credit risk score.  
It provides two scoring modes:

1. **Basic Scoring** — evaluates based on applicant information only.  
2. **Advanced Scoring** — uses applicant information **plus** an uploaded **bank statement** for deeper financial analysis.

---

## 🚀 Base URL


---

## 🔹 1. Basic Scoring (Without Bank Statement)

### **Endpoint**

### **Description**
Accepts basic applicant information such as age, income, loan amount, and credit score,  
and returns a predicted credit score or risk category.

### **Request Example**
```bash

POST /score {without statement}
curl --location 'http://localhost:8000/score' \
--header 'Content-Type: application/json' \
--data '{
    "age": 30,
    "income": 100000,
    "loan_amount": 500000,
    "employment_type": "Salaried",
    "credit_score": 720,
    "existing_debt": 100000
  }'



POST /score/with-statement


curl --location 'http://localhost:8000/score/with-statement' \
--form 'bank_statement=@"/Users/macbook/Downloads/4020202509090704246186.pdf"' \
--form 'age="30"' \
--form 'income="10000"' \
--form 'loan_amount="500000"' \
--form 'employment_type="Salaried"' \
--form 'credit_score="720"' \
--form 'existing_debt="100000"'
