import pandas as pd
import joblib
import shap

# Load trained model
model = joblib.load("xgb_model.pkl")

# Get feature names from the model
model_features = model.get_booster().feature_names

def hybrid_risk_score(application: dict) -> dict:
    """
    Hybrid scoring: rule-based + AI prediction + recommendations
    """
    # --- Rule-based initial score ---
    score = 0
    reasons = []

    credit_score = application.get("credit_score", 700)
    income = application.get("income", 50000)
    loan_amount = application.get("loan_amount", 100000)
    employment_type = application.get("employment_type", "Salaried")
    existing_debt = application.get("existing_debt", 0)

    # Rules
    if credit_score < 600:
        score += 50
        reasons.append("Credit score below 600")
    ratio = (loan_amount / income) * 100
    if ratio > 40:
        score += 30
        reasons.append("High loan-to-income ratio")
    if employment_type == "Salaried":
        score -= 20
        reasons.append("Stable employment reduces risk")
    if income < 25000:
        score += 40
        reasons.append("Low income")
    
    # Existing debt rules
    debt_to_income_ratio = (existing_debt / income) * 100 if income > 0 else 0
    if debt_to_income_ratio > 50:
        score += 35
        reasons.append("High existing debt-to-income ratio")
    elif debt_to_income_ratio > 30:
        score += 20
        reasons.append("Moderate existing debt-to-income ratio")
    elif existing_debt > 0:
        score += 5
        reasons.append("Some existing debt")

    # --- AI Prediction ---

    # Convert application dict to DataFrame
    # Map existing_debt to existing_credits for model compatibility
    app_data = application.copy()
    if 'existing_debt' in app_data and 'existing_credits' not in app_data:
        # Convert existing_debt to existing_credits (simple mapping for now)
        # In a real system, you'd want more sophisticated debt-to-credits mapping
        app_data['existing_credits'] = min(int(app_data['existing_debt'] / 50000), 4)  # Scale to 0-4 range
        del app_data['existing_debt']  # Remove the original field
    
    X_app = pd.DataFrame([app_data])

    # One-hot encode categorical columns
    X_app_encoded = pd.get_dummies(X_app)

    # Add missing columns with 0
    for col in model_features:
        if col not in X_app_encoded.columns:
            X_app_encoded[col] = 0

    # Reorder columns to match training
    X_app_encoded = X_app_encoded[model_features]

    # Predict probability of default
    ai_pred = float(model.predict_proba(X_app_encoded)[0][1])

    # Hybrid score
    hybrid_score = float(score * 0.5 + ai_pred * 100 * 0.5)
    if hybrid_score <= 30:
        risk = "Low Risk"
    elif hybrid_score <= 60:
        risk = "Medium Risk"
    else:
        risk = "High Risk"

    # --- Explainability using SHAP ---
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_app_encoded)
    feature_importance = dict(zip(model_features, shap_values[0]))
    top_features = sorted(feature_importance.items(), key=lambda x: abs(x[1]), reverse=True)[:3]
    for f, v in top_features:
        reasons.append(f"Feature {f} contributed {v:.2f} to risk")

    # --- Recommendations ---
    recommendations = []
    if hybrid_score > 70:
        recommendations.append("Reduce loan amount")
    if credit_score < 600:
        recommendations.append("Require collateral")
    if ratio > 40:
        recommendations.append("Ask for guarantor")
    if employment_type != "Salaried":
        recommendations.append("Consider co-applicant")
    if debt_to_income_ratio > 50:
        recommendations.append("Require debt consolidation plan")
    elif debt_to_income_ratio > 30:
        recommendations.append("Consider debt-to-income improvement")

    # --- Return safe JSON ---
    return {
        "rule_score": float(score),
        "ai_score": ai_pred,
        "hybrid_score": hybrid_score,
        "risk": risk,
        "reasons": reasons,
        "recommendations": recommendations
    }
