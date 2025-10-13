from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Body, Request
from pydantic import BaseModel
from enhanced_scoring import enhanced_hybrid_risk_score
import uvicorn
from typing import Optional
import logging
import ollama

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import bank statement processor (lazy import to avoid errors if not available)
try:
    from bank_statement_processor import get_processor
    BANK_STATEMENT_AVAILABLE = True
    logger.info("Bank statement processing enabled")
except ImportError:
    BANK_STATEMENT_AVAILABLE = False
    logger.warning("Bank statement processing not available - install dependencies")

app = FastAPI(
    title="Enhanced NBFC AI Scoring API",
    description="Advanced AI-powered credit scoring for Non-Banking Financial Companies",
    version="2.0.0"
)

# Optional AI summarizer using Ollama (better than HuggingFace)
try:
    # Test if Ollama is available
    ollama.list()
    OLLAMA_AVAILABLE = True
    logger.info("Ollama AI summarizer enabled")
except Exception as e:
    OLLAMA_AVAILABLE = False
    logger.warning(f"Ollama not available: {e}")

class LoanApplication(BaseModel):
    age: int
    income: float
    loan_amount: float
    employment_type: str
    credit_score: int
    existing_debt: float = 0
    # Optional fields for enhanced scoring
    business_type: Optional[str] = None
    years_in_business: Optional[int] = None
    monthly_income: Optional[float] = None
    bank_account_age: Optional[int] = None

class BatchScoringRequest(BaseModel):
    applications: list[LoanApplication]
    batch_id: Optional[str] = None

@app.get("/")
def root():
    features = [
        "Hybrid AI Scoring",
        "Fraud Detection", 
        "Dynamic Pricing",
        "Alternative Data Integration",
        "Portfolio Insights",
        "Real-time Risk Assessment"
    ]
    
    if BANK_STATEMENT_AVAILABLE:
        features.append("Bank Statement Processing & Verification")
    
    if OLLAMA_AVAILABLE:
        features.append("Ollama AI Explanations")
    
    return {
        "message": "Enhanced NBFC AI Scoring API",
        "version": "3.0.0",
        "features": features,
        "bank_statement_enabled": BANK_STATEMENT_AVAILABLE,
        "ollama_enabled": OLLAMA_AVAILABLE
    }

@app.post("/score")
def score_loan(application: LoanApplication):
    """
    **Standard Loan Scoring (JSON)**
    
    ```bash
    curl -X POST "http://localhost:8000/score" \\
      -H "Content-Type: application/json" \\
      -d '{
        "age": 30,
        "income": 50000,
        "loan_amount": 500000,
        "employment_type": "Salaried",
        "credit_score": 720,
        "existing_debt": 100000
      }'
    ```
    """
    try:
        app_data = application.dict()
        statement_provided = False
        
        logger.info("Processing loan application")
        
        # Perform Enhanced Scoring
        result = enhanced_hybrid_risk_score(app_data)
        
        # Add statement verification status
        result['statement_verification'] = {
            "verified": False,
            "message": "No bank statement provided"
        }
        
        # Add Ollama AI Summary
        if OLLAMA_AVAILABLE:
            try:
                text = " ; ".join(result["reasons"] + result["recommendations"])
                prompt = f"""You are a loan officer. Explain this risk assessment to the applicant in 2-3 clear sentences.
                
Score: {result['enhanced_score']:.1f}/100
Risk Level: {result['risk']}
Key Points: {text}

Write a professional, clear explanation suitable for the customer:"""
                
                response = ollama.chat(
                    model="llama3",
                    messages=[{'role': 'user', 'content': prompt}],
                    options={'temperature': 0.3}
                )
                
                result["ai_explanation"] = response['message']['content']
                logger.info("AI explanation generated successfully")
                
            except Exception as e:
                logger.warning(f"Ollama summary generation failed: {e}")
                result["ai_explanation"] = "AI explanation unavailable"
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Scoring error: {e}")
        raise HTTPException(status_code=500, detail=f"Scoring failed: {str(e)}")


@app.post("/score/with-statement")
async def score_with_statement(
    bank_statement: UploadFile = File(...),
    age: int = Form(...),
    income: float = Form(...),
    loan_amount: float = Form(...),
    employment_type: str = Form(...),
    credit_score: int = Form(...),
    existing_debt: float = Form(0),
    ollama_model: str = Form(default="llama3")
):
    """
    **Loan Scoring with Bank Statement Verification**
    
    Upload bank statement PDF/Image along with application data
    
    ```bash
    curl -X POST "http://localhost:8000/score/with-statement" \\
      -F "bank_statement=@statement.pdf" \\
      -F "age=30" \\
      -F "income=50000" \\
      -F "loan_amount=500000" \\
      -F "employment_type=Salaried" \\
      -F "credit_score=720" \\
      -F "existing_debt=100000"
    ```
    """
    try:
        if not BANK_STATEMENT_AVAILABLE:
            raise HTTPException(
                status_code=503,
                detail="Bank statement processing not available. Install: pip install PyPDF2 easyocr Pillow opencv-python-headless"
            )
        
        logger.info(f"Processing loan with bank statement: {bank_statement.filename}")
        
        # Validate file type
        file_ext = bank_statement.filename.split('.')[-1].lower()
        if file_ext not in ['pdf', 'jpg', 'jpeg', 'png']:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {file_ext}. Allowed: pdf, jpg, jpeg, png"
            )
        
        # Read file content
        file_content = await bank_statement.read()
        if len(file_content) == 0:
            raise HTTPException(status_code=400, detail="Empty file uploaded")
        
        logger.info(f"File size: {len(file_content)} bytes")
        
        # Application data
        app_data = {
            "age": age,
            "income": income,
            "loan_amount": loan_amount,
            "employment_type": employment_type,
            "credit_score": credit_score,
            "existing_debt": existing_debt
        }
        
        # Process bank statement
        processor = get_processor(model=ollama_model)
        statement_data = processor.process_statement(file_content, file_ext)
        
        if 'error' in statement_data:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to process statement: {statement_data.get('error_detail', 'Unknown error')}"
            )
        
        # Enrich application with statement data
        app_data = processor.enrich_loan_application(app_data, statement_data)
        logger.info("Application enriched with bank statement data")
        
        # Extract statement metadata before scoring (not for the model)
        statement_metadata = app_data.pop('_statement_metadata', {})
        
        # Perform enhanced scoring (without statement metadata)
        result = enhanced_hybrid_risk_score(app_data)
        
        # Add statement verification details
        result['statement_verification'] = {
            "verified": True,
            "verified_income": statement_data.get('monthly_income_estimate', 0),
            "declared_income": income,
            "income_match": abs(statement_data.get('monthly_income_estimate', 0) - income) < income * 0.2 if income else False,
            "banking_stability": statement_data.get('income_metrics', {}).get('income_stability_score', 0),
            "red_flags": statement_data.get('red_flag_analysis', {}).get('red_flags', []),
            "statement_risk_level": statement_data.get('red_flag_analysis', {}).get('risk_level', 'Unknown'),
            "financial_health_score": statement_data.get('financial_health_score', 0),
            "account_holder": statement_data.get('account_holder_name', 'N/A'),
            "bank_name": statement_data.get('bank_name', 'N/A'),
            "average_balance": statement_data.get('average_monthly_balance', 0)
        }
        
        # Adjust risk score based on statement findings
        statement_risk_score = statement_data.get('red_flag_analysis', {}).get('financial_risk_score', 0)
        if statement_risk_score > 50:
            result['enhanced_score'] = min(result['enhanced_score'] + (statement_risk_score * 0.3), 100)
            result['reasons'].append(f"Bank statement shows high risk indicators ({statement_risk_score}/100)")
        
        # Check income discrepancy
        income_diff = abs(statement_data.get('monthly_income_estimate', 0) - income) if income else 0
        if income and income_diff > income * 0.2:
            result['enhanced_score'] += 15
            result['recommendations'].append("Income verification discrepancy - additional documentation required")
        
        # Recalculate risk category
        if result['enhanced_score'] <= 30:
            result['risk'] = "Low Risk"
        elif result['enhanced_score'] <= 60:
            result['risk'] = "Medium Risk"
        else:
            result['risk'] = "High Risk"
        
        # Add Ollama AI Summary
        if OLLAMA_AVAILABLE:
            try:
                text = " ; ".join(result["reasons"] + result["recommendations"])
                prompt = f"""You are a loan officer. Explain this risk assessment to the applicant in 2-3 clear sentences.
                
Score: {result['enhanced_score']:.1f}/100
Risk Level: {result['risk']}
Key Points: {text}
Bank Statement: Verified

Write a professional, clear explanation suitable for the customer:"""
                
                response = ollama.chat(
                    model=ollama_model,
                    messages=[{'role': 'user', 'content': prompt}],
                    options={'temperature': 0.3}
                )
                
                result["ai_explanation"] = response['message']['content']
                logger.info("AI explanation generated successfully")
                
            except Exception as e:
                logger.warning(f"Ollama summary generation failed: {e}")
                result["ai_explanation"] = "AI explanation unavailable"
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Scoring with statement failed: {e}")
        raise HTTPException(status_code=500, detail=f"Scoring failed: {str(e)}")


@app.post("/score/batch")
def score_loans_batch(request: BatchScoringRequest):
    """
    Batch scoring for multiple applications
    """
    try:
        results = []
        for i, app in enumerate(request.applications):
            try:
                result = enhanced_hybrid_risk_score(app.dict())
                result["application_id"] = i
                results.append(result)
            except Exception as e:
                results.append({
                    "application_id": i,
                    "error": str(e),
                    "status": "failed"
                })
        
        return {
            "batch_id": request.batch_id,
            "total_applications": len(request.applications),
            "successful": len([r for r in results if "error" not in r]),
            "failed": len([r for r in results if "error" in r]),
            "results": results
        }
        
    except Exception as e:
        logger.error(f"Batch scoring error: {e}")
        raise HTTPException(status_code=500, detail=f"Batch scoring failed: {str(e)}")

@app.get("/health")
def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "timestamp": "2024-01-01T00:00:00Z",
        "version": "2.0.0"
    }

@app.get("/model/info")
def model_info():
    """
    Get information about the AI model
    """
    return {
        "model_type": "Enhanced XGBoost + Rules + Alternative Data",
        "features": [
            "Traditional Credit Data",
            "Alternative Data Sources", 
            "Fraud Detection",
            "Income Stability Analysis",
            "Dynamic Pricing"
        ],
        "capabilities": [
            "Real-time Scoring",
            "Batch Processing",
            "Risk Categorization",
            "Portfolio Insights",
            "Regulatory Compliance"
        ]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

