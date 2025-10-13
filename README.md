---
title: NBFC AI Credit Scoring System
emoji: 💳
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
app_port: 7860
---

# 🏦 NBFC AI Credit Scoring System

[![Live Demo](https://img.shields.io/badge/🤗-Open%20in%20Spaces-blue)](https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME)

An advanced AI-powered credit scoring API designed for Non-Banking Financial Companies (NBFCs) with bank statement verification capabilities.

## 🚀 Features

- **Hybrid AI Scoring**: XGBoost + Rule-based scoring for accurate risk assessment
- **Bank Statement Processing**: OCR-based extraction and verification (PDF/Image support)
- **Fraud Detection**: Real-time red flag analysis
- **Alternative Data Integration**: Beyond traditional credit scores
- **Batch Processing**: Score multiple applications simultaneously
- **REST API**: FastAPI-powered endpoints with automatic documentation

## 📊 API Endpoints

### 1. Basic Credit Scoring
```bash
POST /score
```
Score a loan application using traditional credit data.

### 2. Bank Statement Verification
```bash
POST /score/with-statement
```
Enhanced scoring with bank statement upload and verification.

### 3. Batch Processing
```bash
POST /score/batch
```
Process multiple loan applications at once.

### 4. Health Check
```bash
GET /health
```

## 🔗 Interactive Documentation

Once deployed, visit:
- **Swagger UI**: `https://YOUR_SPACE_URL/docs`
- **ReDoc**: `https://YOUR_SPACE_URL/redoc`

## 📝 Example Usage

### Simple Scoring Request

```bash
curl -X POST "https://YOUR_SPACE_URL/score" \
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

### Bank Statement Scoring

```bash
curl -X POST "https://YOUR_SPACE_URL/score/with-statement" \
  -F "bank_statement=@statement.pdf" \
  -F "age=30" \
  -F "income=50000" \
  -F "loan_amount=500000" \
  -F "employment_type=Salaried" \
  -F "credit_score=720" \
  -F "existing_debt=100000"
```

## 🛠️ Technology Stack

- **Framework**: FastAPI
- **ML Models**: XGBoost, Scikit-learn
- **OCR**: EasyOCR
- **Document Processing**: PyPDF2, OpenCV
- **Deployment**: Docker on Hugging Face Spaces

## 📈 Response Format

```json
{
  "enhanced_score": 45.5,
  "risk": "Medium Risk",
  "decision": "Review",
  "reasons": [
    "High DTI ratio (60%)",
    "Good credit score"
  ],
  "recommendations": [
    "Request additional income verification",
    "Consider shorter tenure"
  ],
  "statement_verification": {
    "verified": true,
    "verified_income": 48500,
    "income_match": true,
    "red_flags": []
  }
}
```

## ⚙️ Model Information

The system uses a hybrid approach:
1. **XGBoost Model**: ML-based risk prediction
2. **Rule-based System**: Business logic and compliance checks
3. **Alternative Data**: Banking behavior, transaction patterns
4. **Fraud Detection**: Red flag analysis from bank statements

## 🔒 Privacy & Security

- No data is stored permanently
- All processing happens in-memory
- GDPR and data privacy compliant
- Secure file handling for bank statements

## 📖 Documentation

For detailed API documentation and examples, see:
- `API_USAGE_EXAMPLES.md`
- `BANK_STATEMENT_GUIDE.md`
- Interactive API docs at `/docs`

## 🤝 Use Cases

- **NBFC Loan Origination**: Automated credit assessment
- **Microfinance**: Quick decisions for small loans
- **Digital Lending Platforms**: API integration
- **Financial Inclusion**: Alternative data for thin-file customers

## 📊 Performance

- Average scoring time: < 2 seconds
- Bank statement processing: < 10 seconds
- Support for PDF and image formats
- Batch processing available

## 🐛 Known Limitations

- Ollama AI explanations not available on HF Spaces (cloud limitation)
- Large PDF files (>10MB) may take longer to process
- OCR accuracy depends on statement quality

## 📄 License

This project is for demonstration and educational purposes.

## 🔗 Links

- [GitHub Repository](https://github.com/YOUR_USERNAME/YOUR_REPO)
- [API Documentation](https://YOUR_SPACE_URL/docs)
- [Contact & Support](mailto:your-email@example.com)

---

Built with ❤️ using FastAPI and deployed on 🤗 Hugging Face Spaces

