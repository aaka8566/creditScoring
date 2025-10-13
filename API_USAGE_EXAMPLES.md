# 📝 Complete API Usage Guide with Examples

## 🎯 Quick Answer

**YES, PDF works!** ✅ Also JPG, PNG images work.

---

## 🚀 How to Call the API

### Method 1: Without Bank Statement (JSON)

```python
import requests

# Your application data
application = {
    "age": 30,
    "income": 50000,
    "loan_amount": 500000,
    "employment_type": "Salaried",
    "credit_score": 720,
    "existing_debt": 100000
}

# Call API
response = requests.post(
    "http://localhost:8000/score",
    json=application,  # Send as JSON
    headers={"Content-Type": "application/json"}
)

# Get result
result = response.json()
print(f"Score: {result['enhanced_score']}")
print(f"Risk: {result['risk']}")
print(f"Statement Verified: {result['statement_verification']['verified']}")
```

---

### Method 2: With Bank Statement PDF (Form Data)

```python
import requests

# Open your PDF file
with open('bank_statement.pdf', 'rb') as pdf_file:
    
    # Application data as form fields
    data = {
        'age': 30,
        'income': 50000,
        'loan_amount': 500000,
        'employment_type': 'Salaried',
        'credit_score': 720,
        'existing_debt': 100000
    }
    
    # Files to upload
    files = {
        'bank_statement': pdf_file  # The PDF file
    }
    
    # Call API
    response = requests.post(
        "http://localhost:8000/score",
        data=data,   # Form data
        files=files  # File upload
    )

# Get result
result = response.json()

# Check if statement was processed
if result['statement_verification']['verified']:
    print("✅ Bank Statement Verified!")
    print(f"   Verified Income: ₹{result['statement_verification']['verified_income']:,.2f}")
    print(f"   Declared Income: ₹{result['statement_verification']['declared_income']:,.2f}")
    print(f"   Income Match: {result['statement_verification']['income_match']}")
    print(f"   Banking Stability: {result['statement_verification']['banking_stability']}/100")
    print(f"   Bank: {result['statement_verification']['bank_name']}")
    print(f"   Average Balance: ₹{result['statement_verification']['average_balance']:,.2f}")
    print(f"   Red Flags: {len(result['statement_verification']['red_flags'])}")
else:
    print("❌ Statement not verified")
```

---

### Method 3: Complete Working Example

```python
import requests
import json

def score_loan(age, income, loan_amount, employment_type, credit_score, 
               existing_debt=0, bank_statement_path=None):
    """
    Score a loan application with optional bank statement
    
    Args:
        age: Applicant age
        income: Monthly income
        loan_amount: Requested loan amount
        employment_type: Employment type (Salaried, Self-Employed, etc.)
        credit_score: Credit score
        existing_debt: Existing debt amount
        bank_statement_path: Optional path to bank statement PDF
    
    Returns:
        dict: Scoring result
    """
    
    url = "http://localhost:8000/score"
    
    if bank_statement_path:
        # With bank statement - use form data
        with open(bank_statement_path, 'rb') as f:
            response = requests.post(
                url,
                data={
                    'age': age,
                    'income': income,
                    'loan_amount': loan_amount,
                    'employment_type': employment_type,
                    'credit_score': credit_score,
                    'existing_debt': existing_debt
                },
                files={'bank_statement': f}
            )
    else:
        # Without bank statement - use JSON
        response = requests.post(
            url,
            json={
                'age': age,
                'income': income,
                'loan_amount': loan_amount,
                'employment_type': employment_type,
                'credit_score': credit_score,
                'existing_debt': existing_debt
            }
        )
    
    return response.json()


# Example 1: Without statement
print("="*60)
print("Example 1: Regular Scoring (No Statement)")
print("="*60)
result1 = score_loan(
    age=30,
    income=50000,
    loan_amount=500000,
    employment_type="Salaried",
    credit_score=720,
    existing_debt=100000
)
print(f"Score: {result1['enhanced_score']:.2f}")
print(f"Risk: {result1['risk']}")
print(f"Statement Verified: {result1['statement_verification']['verified']}")


# Example 2: With statement
print("\n" + "="*60)
print("Example 2: With Bank Statement")
print("="*60)
result2 = score_loan(
    age=30,
    income=50000,
    loan_amount=500000,
    employment_type="Salaried",
    credit_score=720,
    existing_debt=100000,
    bank_statement_path="bank_statement.pdf"  # Your PDF file
)
print(f"Score: {result2['enhanced_score']:.2f}")
print(f"Risk: {result2['risk']}")
print(f"Statement Verified: {result2['statement_verification']['verified']}")
if result2['statement_verification']['verified']:
    print(f"Verified Income: ₹{result2['statement_verification']['verified_income']:,.2f}")
    print(f"Banking Stability: {result2['statement_verification']['banking_stability']}/100")
```

---

## 🏦 Bank Statement Structure

### What the PDF Should Contain

Your bank statement PDF should have these elements (typical Indian bank format):

```
╔════════════════════════════════════════════════════════════╗
║                     HDFC BANK LIMITED                      ║
║                   Account Statement                        ║
╠════════════════════════════════════════════════════════════╣
║                                                            ║
║  Account Holder: Rajesh Kumar                             ║
║  Account Number: XXXX-XXXX-1234                           ║
║  Statement Period: January 2024 - March 2024              ║
║  Branch: Mumbai - Andheri West                            ║
║                                                            ║
║  Opening Balance (01-Jan-2024): ₹25,000.00               ║
║  Closing Balance (31-Mar-2024): ₹45,000.00               ║
║                                                            ║
╠════════════════════════════════════════════════════════════╣
║                 Transaction Details                        ║
╠════════════════════════════════════════════════════════════╣
║                                                            ║
║  Date      Description           Debit      Credit  Balance║
║  ────────  ─────────────────    ────────   ─────── ────────║
║  05-Jan    SALARY CREDIT                   50,000  75,000  ║
║  06-Jan    RENT PAYMENT         25,000             50,000  ║
║  10-Jan    GROCERY STORE         3,500             46,500  ║
║  15-Jan    LOAN EMI             12,000             34,500  ║
║  20-Jan    ELECTRICITY BILL      2,000             32,500  ║
║                                                            ║
║  05-Feb    SALARY CREDIT                   50,000  82,500  ║
║  06-Feb    RENT PAYMENT         25,000             57,500  ║
║  15-Feb    LOAN EMI             12,000             45,500  ║
║                                                            ║
║  05-Mar    SALARY CREDIT                   50,000  95,500  ║
║  06-Mar    RENT PAYMENT         25,000             70,500  ║
║  15-Mar    LOAN EMI             12,000             58,500  ║
║  25-Mar    MEDICAL EXPENSE       8,000             50,500  ║
║                                                            ║
╠════════════════════════════════════════════════════════════╣
║                      Summary                               ║
╠════════════════════════════════════════════════════════════╣
║                                                            ║
║  Total Credits:  ₹1,50,000.00                             ║
║  Total Debits:   ₹1,29,500.00                             ║
║  No. of Transactions: 15                                   ║
║  Average Balance: ₹55,000.00                              ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
```

### What the AI Extracts

From the above statement, Ollama will extract:

```json
{
  "account_holder_name": "Rajesh Kumar",
  "bank_name": "HDFC Bank",
  "account_number": "1234",
  "statement_period": "January 2024 - March 2024",
  "opening_balance": 25000.0,
  "closing_balance": 45000.0,
  "average_monthly_balance": 55000.0,
  "total_credits": 150000.0,
  "total_debits": 129500.0,
  "salary_credits": [50000, 50000, 50000],
  "number_of_salary_credits": 3,
  "monthly_income_estimate": 50000.0,
  "loan_emi_payments": 12000.0,
  "bounced_transactions": 0,
  "cash_deposits": 0,
  "minimum_balance": 32500.0,
  "maximum_balance": 95500.0,
  "financial_health_score": 85
}
```

---

## 📄 Supported Bank Statement Formats

### ✅ Works With

| Bank | Format | Status | Notes |
|------|--------|--------|-------|
| **HDFC Bank** | PDF | ✅ Excellent | Best results |
| **ICICI Bank** | PDF | ✅ Excellent | Best results |
| **SBI** | PDF | ✅ Good | Works well |
| **Axis Bank** | PDF | ✅ Good | Works well |
| **Kotak Mahindra** | PDF | ✅ Good | Works well |
| **Any Bank** | Scanned PDF | ✅ Good | Needs good quality |
| **Any Bank** | JPG/PNG Image | ✅ Moderate | OCR dependent |

### 📋 Minimum Requirements

Your bank statement PDF must have:

1. ✅ **Account holder name**
2. ✅ **Bank name**
3. ✅ **Account number** (partial is fine)
4. ✅ **Statement period** (dates)
5. ✅ **Transaction list** with:
   - Dates
   - Descriptions
   - Amounts (debit/credit)
   - Balance (optional but helpful)
6. ✅ **Opening/Closing balance** (or can be calculated)

### ⚠️ Quality Guidelines

For best results:

- **PDF Quality**: Clear text, not blurry
- **Scanned Images**: 300 DPI or higher
- **File Size**: < 10MB for PDFs, < 5MB for images
- **Language**: English or Hindi text
- **Pages**: 1-10 pages (3 months recommended)

---

## 🧪 Testing Examples

### Test 1: Simple cURL (No Statement)

```bash
curl -X POST "http://localhost:8000/score" \
  -H "Content-Type: application/json" \
  -d '{
    "age": 30,
    "income": 50000,
    "loan_amount": 500000,
    "employment_type": "Salaried",
    "credit_score": 720,
    "existing_debt": 100000
  }'
```

### Test 2: cURL with PDF

```bash
curl -X POST "http://localhost:8000/score" \
  -F "bank_statement=@/path/to/your/statement.pdf" \
  -F "age=30" \
  -F "income=50000" \
  -F "loan_amount=500000" \
  -F "employment_type=Salaried" \
  -F "credit_score=720" \
  -F "existing_debt=100000"
```

### Test 3: Python with Actual File

```python
import requests

# Path to your actual bank statement
statement_path = "/Users/macbook/Documents/bank_statement_jan2024.pdf"

# Application details
with open(statement_path, 'rb') as f:
    response = requests.post(
        "http://localhost:8000/score",
        data={
            'age': 35,
            'income': 75000,
            'loan_amount': 1000000,
            'employment_type': 'Salaried',
            'credit_score': 750,
            'existing_debt': 200000
        },
        files={'bank_statement': f}
    )

result = response.json()

# Pretty print the result
import json
print(json.dumps(result, indent=2))
```

---

## 🌐 Frontend Integration (React)

### Complete React Component

```javascript
import React, { useState } from 'react';
import axios from 'axios';

function LoanApplicationForm() {
  const [formData, setFormData] = useState({
    age: '',
    income: '',
    loan_amount: '',
    employment_type: 'Salaried',
    credit_score: '',
    existing_debt: ''
  });
  
  const [bankStatement, setBankStatement] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      let response;
      
      if (bankStatement) {
        // With bank statement - use FormData
        const formDataObj = new FormData();
        formDataObj.append('bank_statement', bankStatement);
        formDataObj.append('age', formData.age);
        formDataObj.append('income', formData.income);
        formDataObj.append('loan_amount', formData.loan_amount);
        formDataObj.append('employment_type', formData.employment_type);
        formDataObj.append('credit_score', formData.credit_score);
        formDataObj.append('existing_debt', formData.existing_debt || 0);
        
        response = await axios.post('http://localhost:8000/score', formDataObj, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
      } else {
        // Without bank statement - use JSON
        response = await axios.post('http://localhost:8000/score', formData, {
          headers: { 'Content-Type': 'application/json' }
        });
      }
      
      setResult(response.data);
    } catch (error) {
      console.error('Error:', error);
      alert('Failed to process application');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="loan-form">
      <h2>Loan Application</h2>
      
      <form onSubmit={handleSubmit}>
        <input
          type="number"
          placeholder="Age"
          value={formData.age}
          onChange={(e) => setFormData({...formData, age: e.target.value})}
          required
        />
        
        <input
          type="number"
          placeholder="Monthly Income"
          value={formData.income}
          onChange={(e) => setFormData({...formData, income: e.target.value})}
          required
        />
        
        <input
          type="number"
          placeholder="Loan Amount"
          value={formData.loan_amount}
          onChange={(e) => setFormData({...formData, loan_amount: e.target.value})}
          required
        />
        
        <select
          value={formData.employment_type}
          onChange={(e) => setFormData({...formData, employment_type: e.target.value})}
        >
          <option value="Salaried">Salaried</option>
          <option value="Self-Employed">Self-Employed</option>
          <option value="Business">Business</option>
        </select>
        
        <input
          type="number"
          placeholder="Credit Score"
          value={formData.credit_score}
          onChange={(e) => setFormData({...formData, credit_score: e.target.value})}
          required
        />
        
        <input
          type="number"
          placeholder="Existing Debt (optional)"
          value={formData.existing_debt}
          onChange={(e) => setFormData({...formData, existing_debt: e.target.value})}
        />
        
        <div className="file-upload">
          <label>Bank Statement (Optional - PDF/JPG/PNG):</label>
          <input
            type="file"
            accept=".pdf,.jpg,.jpeg,.png"
            onChange={(e) => setBankStatement(e.target.files[0])}
          />
          {bankStatement && <p>✅ File selected: {bankStatement.name}</p>}
        </div>
        
        <button type="submit" disabled={loading}>
          {loading ? 'Processing...' : 'Score Application'}
        </button>
      </form>
      
      {result && (
        <div className="result">
          <h3>Scoring Result</h3>
          <p><strong>Risk Score:</strong> {result.enhanced_score.toFixed(2)}/100</p>
          <p><strong>Risk Level:</strong> {result.risk}</p>
          
          {result.statement_verification.verified && (
            <div className="statement-verification">
              <h4>✅ Bank Statement Verified</h4>
              <p>Verified Income: ₹{result.statement_verification.verified_income.toLocaleString()}</p>
              <p>Banking Stability: {result.statement_verification.banking_stability}/100</p>
              <p>Bank: {result.statement_verification.bank_name}</p>
              <p>Red Flags: {result.statement_verification.red_flags.length}</p>
            </div>
          )}
          
          {result.ai_explanation && (
            <div className="ai-explanation">
              <h4>AI Explanation</h4>
              <p>{result.ai_explanation}</p>
            </div>
          )}
          
          <div className="recommendations">
            <h4>Recommendations</h4>
            <ul>
              {result.recommendations.map((rec, i) => (
                <li key={i}>{rec}</li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}

export default LoanApplicationForm;
```

---

## 📱 Mobile App (React Native)

```javascript
import React, { useState } from 'react';
import { View, Button, Text } from 'react-native';
import DocumentPicker from 'react-native-document-picker';
import axios from 'axios';

function LoanScore() {
  const [result, setResult] = useState(null);

  const pickAndScoreWithStatement = async () => {
    try {
      // Pick PDF file
      const file = await DocumentPicker.pick({
        type: [DocumentPicker.types.pdf, DocumentPicker.types.images],
      });

      // Create form data
      const formData = new FormData();
      formData.append('bank_statement', {
        uri: file[0].uri,
        type: file[0].type,
        name: file[0].name,
      });
      formData.append('age', '30');
      formData.append('income', '50000');
      formData.append('loan_amount', '500000');
      formData.append('employment_type', 'Salaried');
      formData.append('credit_score', '720');

      // Submit
      const response = await axios.post('http://your-api.com/score', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      setResult(response.data);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <View>
      <Button title="Upload Statement & Score" onPress={pickAndScoreWithStatement} />
      {result && (
        <Text>Score: {result.enhanced_score}</Text>
      )}
    </View>
  );
}
```

---

## ❓ Common Questions

### Q: What if my PDF is password protected?
**A:** You need to unlock it first. The API cannot process encrypted PDFs.

### Q: Can I send multiple pages?
**A:** Yes! The API processes multi-page PDFs automatically.

### Q: What if the PDF has images only (scanned)?
**A:** It will work but accuracy depends on image quality. Use 300 DPI+ scans.

### Q: Which format is best?
**A:** Native PDF from bank's website is best. Scanned PDF is second best.

### Q: How long does processing take?
**A:** 
- Without statement: < 1 second
- With PDF: 2-5 seconds
- With image: 5-10 seconds

### Q: What if income doesn't match?
**A:** If verified income differs >20% from declared, the API will flag it and adjust the risk score.

### Q: Does it support Hindi text?
**A:** Yes! The OCR engine supports both English and Hindi.

---

## 🎉 Quick Summary

### Call API WITHOUT Statement
```python
requests.post("http://localhost:8000/score", json={...})
```

### Call API WITH Statement
```python
requests.post("http://localhost:8000/score", 
    data={...},      # Form fields
    files={...}      # PDF file
)
```

### What PDF Should Have
- Account holder name
- Bank name  
- Transactions with dates and amounts
- Balance information
- 3 months of data recommended

### PDF Requirements
- ✅ Format: PDF, JPG, PNG
- ✅ Size: < 10MB
- ✅ Quality: Clear, readable text
- ✅ Language: English or Hindi

**That's it! You're ready to use the API! 🚀**

