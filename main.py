from fastapi import FastAPI
from pydantic import BaseModel
from scoring import hybrid_risk_score
from transformers import pipeline

app = FastAPI(title="Hybrid Loan Risk Scoring API with Recommendations")

# Optional AI summarizer
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

class LoanApplication(BaseModel):
    age: int
    income: float
    loan_amount: float
    employment_type: str
    credit_score: int
    existing_debt: float = 0

@app.post("/score")
def score_loan(application: LoanApplication):
    result = hybrid_risk_score(application.dict())
    # AI-generated human-readable summary
    text = " ; ".join(result["reasons"] + result["recommendations"])
    prompt = f"Applicant risk summary (score {result['hybrid_score']:.1f}, risk {result['risk']}): {text}. Summarize in 2 sentences."
    summary = summarizer(prompt, max_length=70, min_length=20, do_sample=False)
    result["summary"] = summary[0]['summary_text']
    return result
