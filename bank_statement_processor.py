"""
Bank Statement Data Extraction Module
Extracts financial data from bank statements using OCR + Ollama AI
"""

import re
import json
from typing import Dict, List, Optional, Union
from datetime import datetime
import logging
import ollama
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BankStatementProcessor:
    """
    Process bank statements to extract financial data for credit scoring
    """
    
    def __init__(self, ollama_model: str = "llama3"):
        """
        Initialize processor with Ollama model
        
        Args:
            ollama_model: Model to use for text analysis (llama3.2, mistral, etc.)
        """
        self.ollama_model = ollama_model
        logger.info(f"Initialized BankStatementProcessor with model: {ollama_model}")
    
    def extract_text_from_pdf(self, pdf_content: bytes) -> str:
        """
        Extract text from PDF using PyPDF2 (basic) or pymupdf (advanced)
        
        Args:
            pdf_content: Binary content of PDF file
            
        Returns:
            Extracted text
        """
        try:
            import PyPDF2
            from io import BytesIO
            
            pdf_file = BytesIO(pdf_content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            logger.info(f"Extracted {len(text)} characters from PDF")
            return text
            
        except Exception as e:
            logger.error(f"PDF extraction failed: {e}")
            raise Exception(f"Failed to extract text from PDF: {str(e)}")
    
    def extract_text_from_image(self, image_content: bytes) -> str:
        """
        Extract text from image using EasyOCR (better for Indian banks)
        
        Args:
            image_content: Binary content of image file
            
        Returns:
            Extracted text
        """
        try:
            import easyocr
            from io import BytesIO
            from PIL import Image
            import numpy as np
            
            # Initialize EasyOCR reader (supports English + Hindi)
            reader = easyocr.Reader(['en', 'hi'])
            
            # Convert bytes to image
            image = Image.open(BytesIO(image_content))
            image_array = np.array(image)
            
            # Perform OCR
            results = reader.readtext(image_array)
            
            # Combine text
            text = "\n".join([result[1] for result in results])
            
            logger.info(f"Extracted {len(text)} characters from image")
            return text
            
        except Exception as e:
            logger.error(f"Image OCR failed: {e}")
            raise Exception(f"Failed to extract text from image: {str(e)}")
    
    def analyze_with_ollama(self, text: str) -> Dict:
        """
        Use Ollama to extract structured financial data from text
        
        Args:
            text: Raw text from bank statement
            
        Returns:
            Structured financial data
        """
        prompt = f"""You are a financial data extraction expert. Extract financial data from this bank statement.

Bank Statement Text:
{text[:3000]}

Return ONLY valid JSON with these exact fields (no other text):
{{
    "account_holder_name": "string",
    "bank_name": "string",
    "account_number": "string (last 4 digits only)",
    "statement_period": "string (e.g., Jan 2024 - Mar 2024)",
    "opening_balance": float,
    "closing_balance": float,
    "average_monthly_balance": float,
    "total_credits": float,
    "total_debits": float,
    "salary_credits": [list of salary amounts],
    "number_of_salary_credits": int,
    "bounced_transactions": int,
    "loan_emi_payments": float,
    "cash_deposits": float,
    "ecommerce_transactions": int,
    "minimum_balance": float,
    "maximum_balance": float,
    "overdraft_instances": int,
    "financial_health_score": float (0-100),
    "risk_indicators": [list of red flags if any],
    "monthly_income_estimate": float
}}

Rules:
- Return ONLY the JSON object, no explanations
- Use 0 for missing numbers, [] for missing arrays, "" for missing text
- All amounts in Indian Rupees
- Identify salary credits and calculate monthly income
- If data not found, use reasonable defaults

JSON only:"""
        
        try:
            # Call Ollama API
            response = ollama.chat(
                model=self.ollama_model,
                messages=[{
                    'role': 'user',
                    'content': prompt
                }],
                options={
                    'temperature': 0.2,
                    'num_predict': 2000
                },
                format='json'  # Request JSON format from Ollama
            )
            
            # Extract JSON from response
            response_text = response['message']['content']
            
            # Clean up common JSON formatting issues
            response_text = response_text.strip()
            
            # Try to find JSON in response (handle markdown code blocks)
            json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
            else:
                # Try to find raw JSON
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if json_match:
                    json_str = json_match.group()
                else:
                    json_str = response_text
            
            # Try to parse
            try:
                data = json.loads(json_str)
            except json.JSONDecodeError:
                # Try to fix common issues
                json_str = json_str.replace("'", '"')  # Replace single quotes
                json_str = re.sub(r',(\s*[}\]])', r'\1', json_str)  # Remove trailing commas
                data = json.loads(json_str)
            
            logger.info("Successfully extracted structured data using Ollama")
            return data
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Ollama response as JSON: {e}")
            logger.error(f"Response was: {response_text[:500] if 'response_text' in locals() else 'N/A'}")
            
            # Return basic structure with error
            return {
                "error": "Failed to parse statement",
                "error_detail": f"JSON parsing error: {str(e)}. The AI response was not valid JSON.",
                "raw_response": response_text[:500] if 'response_text' in locals() else "No response"
            }
            
        except Exception as e:
            logger.error(f"Ollama analysis failed: {e}")
            raise Exception(f"Failed to analyze with Ollama: {str(e)}")
    
    def calculate_income_metrics(self, statement_data: Dict) -> Dict:
        """
        Calculate additional income stability metrics
        
        Args:
            statement_data: Parsed bank statement data
            
        Returns:
            Income stability metrics
        """
        try:
            salary_credits = statement_data.get('salary_credits', [])
            total_credits = statement_data.get('total_credits', 0)
            
            if not salary_credits:
                return {
                    "income_stability_score": 0,
                    "income_consistency": "Unknown",
                    "irregular_income_flag": True
                }
            
            # Calculate consistency
            avg_salary = sum(salary_credits) / len(salary_credits) if salary_credits else 0
            variance = sum([(x - avg_salary) ** 2 for x in salary_credits]) / len(salary_credits) if salary_credits else 0
            std_dev = variance ** 0.5
            
            # Coefficient of variation (lower is better)
            cv = (std_dev / avg_salary * 100) if avg_salary > 0 else 100
            
            # Score based on consistency (0-100)
            if cv < 10:
                stability_score = 90
                consistency = "Very Stable"
            elif cv < 20:
                stability_score = 75
                consistency = "Stable"
            elif cv < 40:
                stability_score = 50
                consistency = "Moderate"
            else:
                stability_score = 25
                consistency = "Unstable"
            
            return {
                "income_stability_score": stability_score,
                "income_consistency": consistency,
                "average_monthly_salary": avg_salary,
                "salary_variance": cv,
                "irregular_income_flag": cv > 40,
                "number_of_income_sources": len(salary_credits)
            }
            
        except Exception as e:
            logger.error(f"Income metrics calculation failed: {e}")
            return {
                "income_stability_score": 0,
                "income_consistency": "Error",
                "irregular_income_flag": True
            }
    
    def detect_red_flags(self, statement_data: Dict) -> Dict:
        """
        Detect financial red flags from bank statement
        
        Args:
            statement_data: Parsed bank statement data
            
        Returns:
            Red flag analysis
        """
        red_flags = []
        risk_score = 0
        
        # Check for bounced transactions
        bounced = statement_data.get('bounced_transactions', 0)
        if bounced > 0:
            red_flags.append(f"{bounced} bounced transaction(s)")
            risk_score += bounced * 15
        
        # Check for overdraft
        overdraft = statement_data.get('overdraft_instances', 0)
        if overdraft > 0:
            red_flags.append(f"{overdraft} overdraft instance(s)")
            risk_score += overdraft * 10
        
        # Check for low balance
        min_balance = statement_data.get('minimum_balance', 0)
        if min_balance < 5000:
            red_flags.append(f"Low minimum balance: ₹{min_balance:,.2f}")
            risk_score += 20
        
        # Check for high cash deposits (potential undeclared income)
        cash_deposits = statement_data.get('cash_deposits', 0)
        total_credits = statement_data.get('total_credits', 1)
        if cash_deposits > total_credits * 0.3:
            red_flags.append(f"High cash deposits: ₹{cash_deposits:,.2f}")
            risk_score += 25
        
        # Check for EMI burden
        emi_payments = statement_data.get('loan_emi_payments', 0)
        monthly_income = statement_data.get('monthly_income_estimate', 1)
        emi_ratio = (emi_payments / monthly_income * 100) if monthly_income > 0 else 0
        if emi_ratio > 50:
            red_flags.append(f"High EMI burden: {emi_ratio:.1f}% of income")
            risk_score += 30
        
        # Classify risk level
        if risk_score < 30:
            risk_level = "Low"
        elif risk_score < 60:
            risk_level = "Medium"
        else:
            risk_level = "High"
        
        return {
            "red_flags": red_flags,
            "red_flag_count": len(red_flags),
            "financial_risk_score": min(risk_score, 100),
            "risk_level": risk_level,
            "requires_manual_review": risk_score > 50
        }
    
    def process_statement(
        self, 
        file_content: bytes, 
        file_type: str
    ) -> Dict:
        """
        Main processing pipeline for bank statements
        
        Args:
            file_content: Binary content of uploaded file
            file_type: File extension (pdf, jpg, png, etc.)
            
        Returns:
            Complete analysis with financial data and risk indicators
        """
        try:
            logger.info(f"Processing bank statement of type: {file_type}")
            
            # Step 1: Extract text based on file type
            if file_type.lower() == 'pdf':
                text = self.extract_text_from_pdf(file_content)
            elif file_type.lower() in ['jpg', 'jpeg', 'png']:
                text = self.extract_text_from_image(file_content)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
            
            if not text or len(text) < 100:
                raise Exception("Insufficient text extracted from document")
            
            # Step 2: Analyze with Ollama
            statement_data = self.analyze_with_ollama(text)
            
            if 'error' in statement_data:
                return statement_data
            
            # Step 3: Calculate income metrics
            income_metrics = self.calculate_income_metrics(statement_data)
            
            # Step 4: Detect red flags
            red_flag_analysis = self.detect_red_flags(statement_data)
            
            # Step 5: Combine all data
            result = {
                **statement_data,
                "income_metrics": income_metrics,
                "red_flag_analysis": red_flag_analysis,
                "processing_timestamp": datetime.now().isoformat(),
                "data_quality": "high" if not red_flag_analysis['requires_manual_review'] else "medium"
            }
            
            logger.info("Bank statement processing completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Statement processing failed: {e}")
            return {
                "error": "Processing failed",
                "error_detail": str(e),
                "processing_timestamp": datetime.now().isoformat()
            }
    
    def enrich_loan_application(
        self, 
        application_data: Dict, 
        statement_data: Dict
    ) -> Dict:
        """
        Enrich loan application with bank statement data
        
        Args:
            application_data: Original loan application
            statement_data: Parsed bank statement data
            
        Returns:
            Enhanced application data
        """
        try:
            # Only add numeric/scalar values that the XGBoost model can handle
            # Do NOT add lists or complex objects
            
            # Update income with actual statement data
            if 'monthly_income_estimate' in statement_data:
                verified_income = statement_data['monthly_income_estimate']
                # Use verified income if it's reasonable (not 0 or negative)
                if verified_income > 0:
                    application_data['income'] = verified_income
            
            # Calculate revised debt from actual EMI payments
            existing_emi = statement_data.get('loan_emi_payments', 0)
            if existing_emi > 0:
                application_data['existing_debt'] = max(
                    application_data.get('existing_debt', 0),
                    existing_emi * 12  # Annual debt from EMI
                )
            
            # Store statement data separately for later use (not for model scoring)
            # These will be used in the API response but not passed to XGBoost
            application_data['_statement_metadata'] = {
                'average_balance': statement_data.get('average_monthly_balance', 0),
                'banking_stability_score': statement_data.get('income_metrics', {}).get('income_stability_score', 0),
                'statement_risk_score': statement_data.get('red_flag_analysis', {}).get('financial_risk_score', 0),
                'red_flags': statement_data.get('red_flag_analysis', {}).get('red_flags', []),
                'bounced_transactions': statement_data.get('bounced_transactions', 0),
                'overdraft_instances': statement_data.get('overdraft_instances', 0)
            }
            
            logger.info("Successfully enriched loan application with statement data")
            return application_data
            
        except Exception as e:
            logger.error(f"Application enrichment failed: {e}")
            return application_data


# Singleton instance
_processor = None

def get_processor(model: str = "llama3") -> BankStatementProcessor:
    """Get or create processor instance"""
    global _processor
    if _processor is None:
        _processor = BankStatementProcessor(ollama_model=model)
    return _processor

