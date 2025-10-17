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
    
    def calculate_emi(self, principal: float, annual_interest_rate: float, tenure_months: int) -> dict:
        """
        Calculate EMI (Equated Monthly Installment) for a loan
        
        Formula: EMI = [P × R × (1+R)^N] / [(1+R)^N - 1]
        Where:
        - P = Principal loan amount
        - R = Monthly interest rate (annual rate / 12 / 100)
        - N = Tenure in months
        """
        if principal <= 0 or tenure_months <= 0:
            return {
                'emi': 0,
                'total_amount': 0,
                'total_interest': 0,
                'error': 'Invalid principal or tenure'
            }
        
        # Convert annual interest rate to monthly rate
        monthly_rate = annual_interest_rate / 12 / 100
        
        # Calculate EMI using the formula
        if monthly_rate == 0:
            # If interest rate is 0, EMI is just principal divided by months
            emi = principal / tenure_months
        else:
            emi = (principal * monthly_rate * pow(1 + monthly_rate, tenure_months)) / \
                  (pow(1 + monthly_rate, tenure_months) - 1)
        
        # Calculate totals
        total_amount = emi * tenure_months
        total_interest = total_amount - principal
        
        return {
            'emi': round(emi, 2),
            'total_amount': round(total_amount, 2),
            'total_interest': round(total_interest, 2),
            'principal': round(principal, 2),
            'interest_rate': annual_interest_rate,
            'tenure_months': tenure_months,
            'tenure_years': round(tenure_months / 12, 1)
        }
    
    def calculate_emi_options(self, loan_amount: float, annual_interest_rate: float, annual_income: float) -> dict:
        """
        Calculate EMI for multiple tenure options and check affordability
        """
        # Convert annual income to monthly
        monthly_income = annual_income / 12
        
        # Common loan tenures (in months)
        tenures = [12, 24, 36, 48, 60]  # 1, 2, 3, 4, 5 years
        
        emi_options = []
        recommended_tenure = None
        
        for tenure in tenures:
            emi_details = self.calculate_emi(loan_amount, annual_interest_rate, tenure)
            emi = emi_details['emi']
            
            # Calculate EMI-to-income ratio
            emi_to_income_ratio = (emi / monthly_income * 100) if monthly_income > 0 else 0
            
            # Check affordability (EMI should be < 40-50% of monthly income)
            if emi_to_income_ratio <= 40:
                affordability = "Comfortable"
            elif emi_to_income_ratio <= 50:
                affordability = "Manageable"
            elif emi_to_income_ratio <= 60:
                affordability = "Tight"
            else:
                affordability = "Unaffordable"
            
            option = {
                'tenure_months': tenure,
                'tenure_years': round(tenure / 12, 1),
                'emi': emi,
                'total_payment': emi_details['total_amount'],
                'total_interest': emi_details['total_interest'],
                'emi_to_income_ratio': round(emi_to_income_ratio, 2),
                'affordability': affordability,
                'recommended': False
            }
            
            # Recommend the shortest affordable tenure
            if affordability in ["Comfortable", "Manageable"] and recommended_tenure is None:
                option['recommended'] = True
                recommended_tenure = tenure
            
            emi_options.append(option)
        
        # If no tenure is affordable, recommend the longest one
        if recommended_tenure is None:
            emi_options[-1]['recommended'] = True
            recommended_tenure = tenures[-1]
        
        # Get the recommended EMI details
        recommended_emi = next(opt for opt in emi_options if opt['recommended'])
        
        return {
            'loan_amount': loan_amount,
            'interest_rate': annual_interest_rate,
            'monthly_income': round(monthly_income, 2),
            'recommended_emi': recommended_emi['emi'],
            'recommended_tenure_months': recommended_tenure,
            'recommended_tenure_years': round(recommended_tenure / 12, 1),
            'emi_options': emi_options,
            'affordability_status': recommended_emi['affordability'],
            'max_affordable_emi': round(monthly_income * 0.5, 2)  # 50% of monthly income
        }
    
    def calculate_loan_amount_recommendation(self, application: dict, score: float, max_exposure: float) -> dict:
        """
        Calculate minimum, maximum, and recommended loan amounts based on risk profile
        """
        credit_score = application.get('credit_score', 700)
        income = application.get('income', 50000)
        employment_type = application.get('employment_type', 'Salaried')
        requested_amount = application.get('loan_amount', 0)
        existing_debt = application.get('existing_debt', 0)
        
        # --- Calculate Minimum Loan Amount ---
        # Base minimum by risk category
        if score <= 30:
            base_minimum = 50000  # Low risk - can process smaller loans economically
        elif score <= 60:
            base_minimum = 100000  # Medium risk - higher minimum to justify costs
        else:
            base_minimum = 150000  # High risk - need substantial amount for risk premium
        
        # Employment type multiplier
        employment_multipliers = {
            'Salaried': 0.8,      # Stable income - lower minimum
            'Business': 1.0,       # Moderate stability
            'Self-Employed': 1.2,  # Less predictable - higher minimum
            'Freelancer': 1.5,     # Unstable - much higher minimum
            'Unemployed': 2.0      # Very high risk
        }
        emp_multiplier = employment_multipliers.get(employment_type, 1.0)
        
        # Credit score adjustment
        if credit_score >= 750:
            credit_multiplier = 0.9   # Excellent credit - lower minimum
        elif credit_score >= 700:
            credit_multiplier = 1.0   # Good credit - standard minimum
        elif credit_score >= 600:
            credit_multiplier = 1.2   # Fair credit - higher minimum
        else:
            credit_multiplier = 1.5   # Poor credit - much higher minimum
        
        # Calculate final minimum (at least 10% of income, but not less than base)
        minimum_loan = max(
            base_minimum * emp_multiplier * credit_multiplier,
            income * 0.1
        )
        
        # Round to nearest 10,000
        minimum_loan = round(minimum_loan / 10000) * 10000
        
        # --- Calculate Maximum Loan Amount ---
        # Use max_exposure from portfolio insights
        maximum_loan = max_exposure
        
        # --- Calculate Recommended Amount ---
        # Safe amount considering existing debt
        debt_to_income = (existing_debt / income) * 100 if income > 0 else 0
        
        if debt_to_income > 50:
            # High debt - very conservative
            safe_loan = max_exposure * 0.6
        elif debt_to_income > 30:
            # Moderate debt - somewhat conservative
            safe_loan = max_exposure * 0.8
        else:
            # Low debt - can use full exposure
            safe_loan = max_exposure
        
        # Recommended is the safer of requested or safe loan
        recommended_loan = min(requested_amount, safe_loan, maximum_loan)
        recommended_loan = max(recommended_loan, 0)
        
        # Round to nearest 10,000
        recommended_loan = round(recommended_loan / 10000) * 10000
        maximum_loan = round(maximum_loan / 10000) * 10000
        
        # --- Decision Logic ---
        decision_reasoning = []
        
        # Case 1: Minimum exceeds Maximum (Unviable)
        if minimum_loan > maximum_loan:
            approval_decision = "REJECT - Unviable"
            actionable_decision = f"REJECT - Minimum required (₹{minimum_loan:,.0f}) exceeds maximum capacity (₹{maximum_loan:,.0f})"
            decision_reasoning.extend([
                f"Minimum viable loan for risk profile: ₹{minimum_loan:,.0f}",
                f"Maximum capacity based on income and debt: ₹{maximum_loan:,.0f}",
                f"Gap: ₹{minimum_loan - maximum_loan:,.0f}",
                "Applicant cannot qualify for minimum economical loan amount"
            ])
            alternative_options = [
                "Reduce existing debt to increase maximum capacity",
                "Add a co-applicant to boost combined income",
                "Improve credit score to reduce minimum requirement",
                "Consider collateral-backed loan to lower minimum threshold"
            ]
        
        # Case 2: Requested amount is too low
        elif requested_amount < minimum_loan:
            approval_decision = "REJECT - Below Minimum"
            actionable_decision = f"REJECT - Requested amount (₹{requested_amount:,.0f}) below minimum threshold (₹{minimum_loan:,.0f})"
            decision_reasoning.extend([
                f"Requested: ₹{requested_amount:,.0f}",
                f"Minimum required: ₹{minimum_loan:,.0f}",
                f"Shortfall: ₹{minimum_loan - requested_amount:,.0f}",
                "Amount too small to process economically for this risk profile"
            ])
            alternative_options = [
                f"Increase loan request to at least ₹{minimum_loan:,.0f}",
                "Improve credit profile to qualify for lower minimums",
                "Consider alternative lenders for micro-loans"
            ]
        
        # Case 3: Requested exceeds maximum
        elif requested_amount > maximum_loan:
            approval_decision = "APPROVE - Reduced Amount"
            actionable_decision = f"APPROVE ₹{recommended_loan:,.0f} (reduced from ₹{requested_amount:,.0f})"
            decision_reasoning.extend([
                f"Requested: ₹{requested_amount:,.0f}",
                f"Maximum safe exposure: ₹{maximum_loan:,.0f}",
                f"Recommended: ₹{recommended_loan:,.0f}",
                f"Reduction: ₹{requested_amount - recommended_loan:,.0f}"
            ])
            if debt_to_income > 30:
                decision_reasoning.append(f"High debt-to-income ratio ({debt_to_income:.1f}%) limits capacity")
            alternative_options = [
                f"Accept reduced amount of ₹{recommended_loan:,.0f}",
                "Reduce existing debt to qualify for higher amount",
                "Add co-applicant to increase borrowing capacity"
            ]
        
        # Case 4: Clean approval
        else:
            approval_decision = "APPROVED - Full Amount"
            actionable_decision = f"APPROVE ₹{requested_amount:,.0f} as requested"
            decision_reasoning.extend([
                f"Requested: ₹{requested_amount:,.0f}",
                f"Within safe range: ₹{minimum_loan:,.0f} - ₹{maximum_loan:,.0f}",
                "All eligibility criteria met"
            ])
            alternative_options = [
                f"Could potentially borrow up to ₹{maximum_loan:,.0f}",
                "Maintain good payment history for future increases"
            ]
        
        return {
            'minimum_loan_amount': float(minimum_loan),
            'maximum_loan_amount': float(maximum_loan),
            'recommended_loan_amount': float(recommended_loan),
            'requested_amount': float(requested_amount),
            'approval_decision': approval_decision,
            'actionable_decision': actionable_decision,
            'decision_reasoning': decision_reasoning,
            'alternative_options': alternative_options,
            'loan_range': f"₹{minimum_loan:,.0f} - ₹{maximum_loan:,.0f}",
            'viable': minimum_loan <= maximum_loan,
            'annual_income': float(income)  # Store for EMI calculation
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
        
        # Loan amount recommendation
        loan_recommendation = self.calculate_loan_amount_recommendation(
            application, 
            hybrid_score, 
            portfolio['max_recommended_exposure']
        )
        
        # EMI Calculation for recommended loan amount
        interest_rate = pricing['final_rate']
        recommended_amount = loan_recommendation['recommended_loan_amount']
        
        # Calculate EMI options for the recommended amount
        if recommended_amount > 0 and loan_recommendation['viable']:
            emi_details = self.calculate_emi_options(
                recommended_amount,
                interest_rate,
                income
            )
        else:
            # If not viable, calculate EMI for requested amount to show why it's unaffordable
            emi_details = self.calculate_emi_options(
                loan_amount if loan_amount > 0 else 50000,  # Default to 50K if 0
                interest_rate,
                income
            )
            # Mark as unaffordable scenario
            emi_details['note'] = "EMI calculated for reference only - loan not approved"
        
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
            "loan_amount_recommendation": loan_recommendation,
            "emi_details": emi_details,
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

