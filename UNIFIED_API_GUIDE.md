# 🎯 Unified API - One Endpoint for Everything

## The Problem You Had

Before: Multiple endpoints were confusing
- `/score` - for regular scoring
- `/statement/upload` - for bank statements  
- `/score/enhanced-with-statement` - for both?

**This was complicated!** 🤯

## The Solution

**ONE endpoint handles EVERYTHING**: `/score`

It intelligently detects:
- ✅ JSON request → Regular scoring
- ✅ Form data + file → Bank statement scoring
- ✅ Form data without file → Regular scoring

---

## 🚀 Usage Examples

### Example 1: Regular Scoring (JSON) - Your Existing Code

```bash
# This works EXACTLY as before - backward compatible!
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

**Response**:
```json
{
  "enhanced_score": 45.2,
  "risk": "Medium Risk",
  "reasons": ["..."],
  "recommendations": ["..."],
  "statement_verification": {
    "verified": false,
    "message": "No bank statement provided"
  },
  "ai_explanation": "Your application shows moderate risk..."
}
```

---

### Example 2: With Bank Statement (Form Data)

```bash
# Same endpoint, just add the file!
curl -X POST "http://localhost:8000/score" \
  -F "bank_statement=@statement.pdf" \
  -F "age=30" \
  -F "income=50000" \
  -F "loan_amount=500000" \
  -F "employment_type=Salaried" \
  -F "credit_score=720" \
  -F "existing_debt=100000"
```

**Response**:
```json
{
  "enhanced_score": 42.5,
  "risk": "Medium Risk",
  "reasons": ["..."],
  "recommendations": ["..."],
  "statement_verification": {
    "verified": true,
    "verified_income": 48500,
    "declared_income": 50000,
    "income_match": true,
    "banking_stability": 90,
    "red_flags": [],
    "statement_risk_level": "Low",
    "financial_health_score": 85,
    "account_holder": "John Doe",
    "bank_name": "HDFC Bank",
    "average_balance": 45000
  },
  "ai_explanation": "Your verified bank statement shows stable income..."
}
```

---

## 🐍 Python Integration

### Without Bank Statement

```python
import requests

# Your existing code works as-is!
application = {
    "age": 30,
    "income": 50000,
    "loan_amount": 500000,
    "employment_type": "Salaried",
    "credit_score": 720,
    "existing_debt": 100000
}

response = requests.post(
    "http://localhost:8000/score",
    json=application  # JSON format
)

result = response.json()
print(f"Risk Score: {result['enhanced_score']}")
print(f"Risk Level: {result['risk']}")
```

### With Bank Statement

```python
import requests

# Open the file
with open('bank_statement.pdf', 'rb') as f:
    # Use form data instead of JSON
    response = requests.post(
        "http://localhost:8000/score",
        files={'bank_statement': f},
        data={
            'age': 30,
            'income': 50000,
            'loan_amount': 500000,
            'employment_type': 'Salaried',
            'credit_score': 720,
            'existing_debt': 100000
        }
    )

result = response.json()

# Check if statement was verified
if result['statement_verification']['verified']:
    print(f"✅ Income Verified: ₹{result['statement_verification']['verified_income']}")
    print(f"✅ Banking Stability: {result['statement_verification']['banking_stability']}/100")
    print(f"✅ Red Flags: {len(result['statement_verification']['red_flags'])}")
else:
    print("❌ Statement not verified")
```

---

## 🌐 Frontend Integration (React Example)

```javascript
// Without bank statement
const scoreApplication = async (application) => {
  const response = await fetch('http://localhost:8000/score', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(application)
  });
  return response.json();
};

// With bank statement
const scoreWithStatement = async (application, statementFile) => {
  const formData = new FormData();
  
  // Add file
  formData.append('bank_statement', statementFile);
  
  // Add application data
  formData.append('age', application.age);
  formData.append('income', application.income);
  formData.append('loan_amount', application.loan_amount);
  formData.append('employment_type', application.employment_type);
  formData.append('credit_score', application.credit_score);
  formData.append('existing_debt', application.existing_debt);
  
  const response = await fetch('http://localhost:8000/score', {
    method: 'POST',
    body: formData  // No Content-Type header - FormData sets it automatically
  });
  return response.json();
};

// Usage in component
function LoanForm() {
  const [file, setFile] = useState(null);
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    const application = {
      age: 30,
      income: 50000,
      loan_amount: 500000,
      employment_type: 'Salaried',
      credit_score: 720,
      existing_debt: 100000
    };
    
    const result = file 
      ? await scoreWithStatement(application, file)  // With statement
      : await scoreApplication(application);          // Without statement
    
    console.log('Score:', result.enhanced_score);
    console.log('Statement Verified:', result.statement_verification.verified);
  };
  
  return (
    <form onSubmit={handleSubmit}>
      {/* Form fields */}
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button type="submit">Score Application</button>
    </form>
  );
}
```

---

## 🔍 How It Works Internally

```
                        ┌─────────────────────┐
                        │   POST /score       │
                        └──────────┬──────────┘
                                   │
                    ┌──────────────┴──────────────┐
                    │                             │
             JSON Request?               Form Data Request?
                    │                             │
                    │                             │
         ┌──────────▼─────────┐       ┌──────────▼──────────┐
         │  Regular Scoring   │       │   Check for File    │
         │  (Existing Flow)   │       └──────────┬──────────┘
         └──────────┬─────────┘                  │
                    │              ┌─────────────┴────────────┐
                    │              │                          │
                    │         No File                    File Uploaded
                    │              │                          │
                    │         Regular Scoring    ┌───────────▼───────────┐
                    │              │             │ Process Bank Statement│
                    │              │             │  Extract Financial    │
                    │              │             │       Data            │
                    │              │             └───────────┬───────────┘
                    │              │                         │
                    │              │                         │
                    └──────────────┴─────────┬───────────────┘
                                             │
                                   ┌─────────▼──────────┐
                                   │  Enhanced Scoring  │
                                   │  + XGBoost Model   │
                                   │  + Business Rules  │
                                   │  + Statement Data  │
                                   └─────────┬──────────┘
                                             │
                                   ┌─────────▼──────────┐
                                   │   Ollama AI        │
                                   │   Explanation      │
                                   └─────────┬──────────┘
                                             │
                                   ┌─────────▼──────────┐
                                   │   JSON Response    │
                                   └────────────────────┘
```

---

## ✅ Benefits of This Approach

### 1. **Backward Compatible**
Your existing JSON API calls work exactly as before. No breaking changes!

### 2. **One Endpoint**
- No confusion about which endpoint to use
- Easier to document and explain
- Simpler frontend integration

### 3. **Intelligent Detection**
The API automatically detects:
- JSON vs Form Data
- File present or not
- Processes accordingly

### 4. **Graceful Degradation**
If bank statement processing fails, it still returns regular scoring.

### 5. **Progressive Enhancement**
- Start without statements
- Add statement verification later
- No code changes needed!

---

## 📊 Response Structure

### Always Present
```json
{
  "enhanced_score": 45.2,
  "risk": "Medium Risk",
  "rule_score": 30.0,
  "ai_score": 0.52,
  "reasons": ["..."],
  "recommendations": ["..."],
  "fraud_analysis": {...},
  "dynamic_pricing": {...},
  "portfolio_insights": {...},
  "statement_verification": {...},  // Always present
  "ai_explanation": "..."            // If Ollama available
}
```

### Statement Verification (when file uploaded)
```json
{
  "statement_verification": {
    "verified": true,                    // true if processed successfully
    "verified_income": 48500,           // Actual income from statement
    "declared_income": 50000,           // What customer declared
    "income_match": true,               // Within 20% tolerance
    "banking_stability": 90,            // 0-100 score
    "red_flags": [],                    // Array of issues found
    "statement_risk_level": "Low",      // Low/Medium/High
    "financial_health_score": 85,       // 0-100
    "account_holder": "John Doe",
    "bank_name": "HDFC Bank",
    "average_balance": 45000
  }
}
```

### Statement Verification (when no file uploaded)
```json
{
  "statement_verification": {
    "verified": false,
    "message": "No bank statement provided or processing unavailable"
  }
}
```

---

## 🚀 Quick Start

### Step 1: Start the API
```bash
cd /Users/macbook/Desktop/dvaraRepos/scoring
python enhanced_main.py
```

### Step 2: Test Without Statement
```bash
curl -X POST "http://localhost:8000/score" \
  -H "Content-Type: application/json" \
  -d '{"age":30,"income":50000,"loan_amount":500000,"employment_type":"Salaried","credit_score":720}'
```

### Step 3: Test With Statement
```bash
curl -X POST "http://localhost:8000/score" \
  -F "bank_statement=@statement.pdf" \
  -F "age=30" \
  -F "income=50000" \
  -F "loan_amount=500000" \
  -F "employment_type=Salaried" \
  -F "credit_score=720"
```

### Step 4: Check API Status
```bash
curl http://localhost:8000/
```

---

## 🔧 Configuration

### Enable Bank Statement Processing
```bash
# Install dependencies
pip install PyPDF2 easyocr Pillow opencv-python-headless

# Install and start Ollama
brew install ollama
ollama serve

# Pull AI model
ollama pull llama3.2
```

### Verify Everything Works
```bash
curl http://localhost:8000/ | json_pp
```

Should show:
```json
{
  "message": "Enhanced NBFC AI Scoring API",
  "version": "3.0.0",
  "bank_statement_enabled": true,
  "ollama_enabled": true,
  "features": [
    "Hybrid AI Scoring",
    "Fraud Detection",
    "Dynamic Pricing",
    "Alternative Data Integration",
    "Portfolio Insights",
    "Real-time Risk Assessment",
    "Bank Statement Processing & Verification",
    "Ollama AI Explanations"
  ]
}
```

---

## 🎉 Summary

### Before
```
❌ Multiple endpoints
❌ Confusion about which to use
❌ Complex integration
❌ Separate workflows
```

### After
```
✅ ONE unified endpoint: /score
✅ Automatic detection (JSON vs Form)
✅ Optional file upload
✅ Backward compatible
✅ Simple integration
```

**Your API is now production-ready! 🚀**

---

## 📞 Need Help?

### Check Status
```bash
curl http://localhost:8000/
```

### View Interactive Docs
Open: http://localhost:8000/docs

### Test Online
Use the Swagger UI to upload files and test directly in your browser!

---

**That's it! One endpoint, infinite possibilities! 💪**

