import pandas as pd
import joblib
import numpy as np
from datetime import datetime, timedelta
import requests
import json
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

# Load trained model
model = joblib.load("xgb_model.pkl")
model_features = model.get_booster().feature_names

class EnhancedNBFCScoring:
    """
    Enhanced AI scoring system for NBFCs with advanced features
    """
    
    def __init__(self):
        self.model = model
        self.model_features = model_features
        self.fraud_threshold = 0.8
        self.risk_weights = {
            'credit_score': 0.25,
            'debt_ratio': 0.20,
            'income_stability': 0.15,
            'employment': 0.15,
            'age_experience': 0.10,
            'alternative_data': 0.15
        }
    
    def get_alternative_data(self, application: dict) -> dict:
        """
        Simulate alternative data sources (in real implementation, 
        integrate with actual APIs)
        """
        # Simulate social media sentiment analysis
        social_sentiment = np.random.uniform(0.3, 0.9)
        
        # Simulate mobile app usage (if available)
        app_usage_score = np.random.uniform(0.4, 0.95)
        
        # Simulate utility bill payment history
        utility_score = np.random.uniform(0.5, 1.0)
        
        # Simulate e-commerce behavior
        ecommerce_score = np.random.uniform(0.3, 0.9)
        
        return {
            'social_sentiment': social_sentiment,
            'app_usage': app_usage_score,
            'utility_payments': utility_score,
            'ecommerce_behavior': ecommerce_score,
            'alternative_score': (social_sentiment + app_usage_score + 
                                utility_score + ecommerce_score) / 4
        }
    
    def calculate_income_stability(self, application: dict) -> float:
        """
        Calculate income stability score based on employment type and duration
        """
        employment_type = application.get('employment_type', 'Salaried')
        age = application.get('age', 25)
        
        stability_scores = {
            'Salaried': 0.9,
            'Self-Employed': 0.6,
            'Business': 0.7,
            'Freelancer': 0.4,
            'Unemployed': 0.1
        }
        
        # Adjust for age (experience factor)
        experience_factor = min(age / 30, 1.0)  # Peak at 30 years
        
        return stability_scores.get(employment_type, 0.5) * experience_factor
    
    def detect_fraud_indicators(self, application: dict) -> dict:
        """
        Basic fraud detection using rule-based and ML approaches
        """
        fraud_score = 0
        fraud_reasons = []
        
        # Rule-based fraud detection
        income = application.get('income', 0)
        loan_amount = application.get('loan_amount', 0)
        age = application.get('age', 25)
        credit_score = application.get('credit_score', 700)
        
        # Unrealistic income for age
        if age < 25 and income > 1000000:
            fraud_score += 0.3
            fraud_reasons.append("Unrealistic income for age")
        
        # Very high loan-to-income ratio
        if income > 0 and (loan_amount / income) > 10:
            fraud_score += 0.4
            fraud_reasons.append("Extremely high loan-to-income ratio")
        
        # Credit score vs income mismatch
        if credit_score < 500 and income > 500000:
            fraud_score += 0.2
            fraud_reasons.append("Credit score-income mismatch")
        
        # Round numbers (potential fake data)
        if income % 100000 == 0 and income > 100000:
            fraud_score += 0.1
            fraud_reasons.append("Suspicious round income figure")
        
        return {
            'fraud_score': min(fraud_score, 1.0),
            'fraud_reasons': fraud_reasons,
            'is_fraud_risk': fraud_score > self.fraud_threshold
        }
    
    def calculate_dynamic_pricing(self, base_score: float, application: dict) -> dict:
        """
        Calculate dynamic interest rates based on risk profile
        """
        base_rate = 12.0  # Base interest rate for NBFC
        
        # Risk-based adjustments
        if base_score <= 30:
            risk_adjustment = -2.0  # Lower rate for low risk
        elif base_score <= 60:
            risk_adjustment = 0.0   # Base rate
        else:
            risk_adjustment = 3.0   # Higher rate for high risk
        
        # Employment type adjustments
        employment_type = application.get('employment_type', 'Salaried')
        emp_adjustments = {
            'Salaried': -0.5,
            'Self-Employed': 0.5,
            'Business': 0.0,
            'Freelancer': 1.0,
            'Unemployed': 2.0
        }
        
        emp_adjustment = emp_adjustments.get(employment_type, 0.0)
        
        # Loan amount adjustments
        loan_amount = application.get('loan_amount', 0)
        if loan_amount > 1000000:
            amount_adjustment = 0.5
        else:
            amount_adjustment = 0.0
        
        final_rate = base_rate + risk_adjustment + emp_adjustment + amount_adjustment
        final_rate = max(final_rate, 8.0)  # Minimum rate
        final_rate = min(final_rate, 24.0)  # Maximum rate
        
        return {
            'base_rate': base_rate,
            'final_rate': round(final_rate, 2),
            'risk_adjustment': risk_adjustment,
            'employment_adjustment': emp_adjustment,
            'amount_adjustment': amount_adjustment
        }
    
    def generate_portfolio_insights(self, application: dict, score: float) -> dict:
        """
        Generate portfolio-level insights for risk management
        """
        loan_amount = application.get('loan_amount', 0)
        income = application.get('income', 0)
        
        # Portfolio risk categories
        if score <= 30:
            risk_category = "Prime"
            max_exposure = income * 0.8
        elif score <= 60:
            risk_category = "Near-Prime"
            max_exposure = income * 0.6
        else:
            risk_category = "Sub-Prime"
            max_exposure = income * 0.4
        
        # Concentration risk
        concentration_risk = "Low" if loan_amount < max_exposure else "High"
        
        return {
            'risk_category': risk_category,
            'max_recommended_exposure': max_exposure,
            'concentration_risk': concentration_risk,
            'portfolio_allocation': f"Max {int(max_exposure/100000)}L exposure"
        }
    
    def enhanced_risk_score(self, application: dict) -> dict:
        """
        Enhanced scoring with advanced AI features
        """
        # Get alternative data
        alt_data = self.get_alternative_data(application)
        
        # Fraud detection
        fraud_analysis = self.detect_fraud_indicators(application)
        
        # Income stability
        income_stability = self.calculate_income_stability(application)
        
        # Traditional scoring (existing logic)
        score = 0
        reasons = []
        
        credit_score = application.get("credit_score", 700)
        income = application.get("income", 50000)
        loan_amount = application.get("loan_amount", 100000)
        employment_type = application.get("employment_type", "Salaried")
        existing_debt = application.get("existing_debt", 0)
        age = application.get("age", 25)
        
        # Enhanced rules with weights
        if credit_score < 600:
            score += 50
            reasons.append("Credit score below 600")
        elif credit_score < 700:
            score += 25
            reasons.append("Below average credit score")
        
        ratio = (loan_amount / income) * 100 if income > 0 else 0
        if ratio > 40:
            score += 30
            reasons.append("High loan-to-income ratio")
        
        if employment_type == "Salaried":
            score -= 20
            reasons.append("Stable employment reduces risk")
        
        if income < 25000:
            score += 40
            reasons.append("Low income")
        
        # Enhanced debt analysis
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
        
        # Alternative data integration
        if alt_data['alternative_score'] < 0.5:
            score += 15
            reasons.append("Poor alternative data indicators")
        elif alt_data['alternative_score'] > 0.8:
            score -= 10
            reasons.append("Strong alternative data indicators")
        
        # Income stability factor
        if income_stability < 0.5:
            score += 20
            reasons.append("Unstable income profile")
        elif income_stability > 0.8:
            score -= 10
            reasons.append("Very stable income profile")
        
        # AI Model Prediction (existing logic)
        app_data = application.copy()
        if 'existing_debt' in app_data and 'existing_credits' not in app_data:
            app_data['existing_credits'] = min(int(app_data['existing_debt'] / 50000), 4)
            del app_data['existing_debt']
        
        X_app = pd.DataFrame([app_data])
        X_app_encoded = pd.get_dummies(X_app)
        
        for col in self.model_features:
            if col not in X_app_encoded.columns:
                X_app_encoded[col] = 0
        
        X_app_encoded = X_app_encoded[self.model_features]
        ai_pred = float(self.model.predict_proba(X_app_encoded)[0][1])
        
        # Enhanced hybrid scoring with weights
        rule_weight = 0.4
        ai_weight = 0.4
        alt_data_weight = 0.2
        
        hybrid_score = (score * rule_weight + 
                       ai_pred * 100 * ai_weight + 
                       (1 - alt_data['alternative_score']) * 100 * alt_data_weight)
        
        # Risk classification
        if hybrid_score <= 30:
            risk = "Low Risk"
        elif hybrid_score <= 60:
            risk = "Medium Risk"
        else:
            risk = "High Risk"
        
        # Dynamic pricing
        pricing = self.calculate_dynamic_pricing(hybrid_score, application)
        
        # Portfolio insights
        portfolio = self.generate_portfolio_insights(application, hybrid_score)
        
        # Enhanced recommendations
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
        if fraud_analysis['is_fraud_risk']:
            recommendations.append("Additional verification required")
        if alt_data['alternative_score'] < 0.5:
            recommendations.append("Request additional documentation")
        
        return {
            "enhanced_score": float(hybrid_score),
            "risk": risk,
            "rule_score": float(score),
            "ai_score": ai_pred,
            "alternative_data_score": alt_data['alternative_score'],
            "income_stability": income_stability,
            "fraud_analysis": fraud_analysis,
            "dynamic_pricing": pricing,
            "portfolio_insights": portfolio,
            "reasons": reasons,
            "recommendations": recommendations,
            "timestamp": datetime.now().isoformat(),
            "model_version": "enhanced_v1.0"
        }

# Create enhanced scoring instance
enhanced_scorer = EnhancedNBFCScoring()

def enhanced_hybrid_risk_score(application: dict) -> dict:
    """
    Enhanced scoring function for NBFCs
    """
    return enhanced_scorer.enhanced_risk_score(application)

