"""
Simple Test Script for Unified API
Run this to test both scenarios (with and without bank statement)
"""

import requests
import json
import sys
from pathlib import Path

API_URL = "http://localhost:8000"


def print_section(title):
    """Print a nice section header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)


def test_api_health():
    """Check if API is running"""
    print_section("Testing API Health")
    
    try:
        response = requests.get(f"{API_URL}/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API is running!")
            print(f"   Version: {data['version']}")
            print(f"   Bank Statement Enabled: {data['bank_statement_enabled']}")
            print(f"   Ollama Enabled: {data['ollama_enabled']}")
            print(f"\n   Features:")
            for feature in data['features']:
                print(f"   - {feature}")
            return True
        else:
            print(f"❌ API returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to API: {e}")
        print("\n💡 Make sure to start the API first:")
        print("   python enhanced_main.py")
        return False


def test_regular_scoring():
    """Test regular scoring without bank statement"""
    print_section("Test 1: Regular Scoring (No Bank Statement)")
    
    # Sample application
    application = {
        "age": 30,
        "income": 50000,
        "loan_amount": 500000,
        "employment_type": "Salaried",
        "credit_score": 720,
        "existing_debt": 100000
    }
    
    print("\n📝 Application Data:")
    print(json.dumps(application, indent=2))
    
    try:
        print("\n⏳ Sending request...")
        response = requests.post(
            f"{API_URL}/score",
            json=application,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("\n✅ Scoring Successful!")
            print(f"\n📊 Results:")
            print(f"   Risk Score: {result['enhanced_score']:.2f}/100")
            print(f"   Risk Level: {result['risk']}")
            print(f"   Rule Score: {result['rule_score']:.2f}")
            print(f"   AI Score: {result['ai_score']:.2f}")
            
            print(f"\n💡 Reasons:")
            for reason in result.get('reasons', [])[:3]:
                print(f"   - {reason}")
            
            print(f"\n📋 Recommendations:")
            for rec in result.get('recommendations', [])[:3]:
                print(f"   - {rec}")
            
            print(f"\n🏦 Statement Verification:")
            print(f"   Verified: {result['statement_verification']['verified']}")
            print(f"   Message: {result['statement_verification']['message']}")
            
            if 'ai_explanation' in result:
                print(f"\n🤖 AI Explanation:")
                print(f"   {result['ai_explanation']}")
            
            return result
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def test_with_bank_statement(statement_path=None):
    """Test scoring with bank statement"""
    print_section("Test 2: Scoring With Bank Statement")
    
    if statement_path is None:
        print("\n⚠️  No bank statement file provided")
        print("\nTo test with a real PDF, run:")
        print("   python test_api.py /path/to/your/statement.pdf")
        print("\nFor now, showing example code:\n")
        
        example_code = """
import requests

with open('bank_statement.pdf', 'rb') as pdf_file:
    response = requests.post(
        'http://localhost:8000/score',
        data={
            'age': 30,
            'income': 50000,
            'loan_amount': 500000,
            'employment_type': 'Salaried',
            'credit_score': 720,
            'existing_debt': 100000
        },
        files={'bank_statement': pdf_file}
    )
    
result = response.json()
print(f"Score: {result['enhanced_score']}")
print(f"Verified: {result['statement_verification']['verified']}")
if result['statement_verification']['verified']:
    print(f"Verified Income: {result['statement_verification']['verified_income']}")
    print(f"Banking Stability: {result['statement_verification']['banking_stability']}/100")
"""
        print(example_code)
        return None
    
    # Check if file exists
    file_path = Path(statement_path)
    if not file_path.exists():
        print(f"❌ File not found: {statement_path}")
        return None
    
    print(f"\n📄 Using file: {file_path.name}")
    print(f"   Size: {file_path.stat().st_size / 1024:.2f} KB")
    
    # Application data
    application = {
        'age': 30,
        'income': 50000,
        'loan_amount': 500000,
        'employment_type': 'Salaried',
        'credit_score': 720,
        'existing_debt': 100000
    }
    
    print("\n📝 Application Data:")
    for key, value in application.items():
        print(f"   {key}: {value}")
    
    try:
        print("\n⏳ Processing (this may take 5-10 seconds)...")
        
        with open(file_path, 'rb') as f:
            response = requests.post(
                f"{API_URL}/score",
                data=application,
                files={'bank_statement': f}
            )
        
        if response.status_code == 200:
            result = response.json()
            print("\n✅ Scoring Successful!")
            
            print(f"\n📊 Results:")
            print(f"   Risk Score: {result['enhanced_score']:.2f}/100")
            print(f"   Risk Level: {result['risk']}")
            
            print(f"\n🏦 Statement Verification:")
            sv = result['statement_verification']
            print(f"   Verified: {sv['verified']}")
            
            if sv['verified']:
                print(f"   Account Holder: {sv.get('account_holder', 'N/A')}")
                print(f"   Bank: {sv.get('bank_name', 'N/A')}")
                print(f"   Declared Income: ₹{sv.get('declared_income', 0):,.2f}")
                print(f"   Verified Income: ₹{sv.get('verified_income', 0):,.2f}")
                print(f"   Income Match: {'✅ Yes' if sv.get('income_match') else '❌ No'}")
                print(f"   Banking Stability: {sv.get('banking_stability', 0)}/100")
                print(f"   Average Balance: ₹{sv.get('average_balance', 0):,.2f}")
                print(f"   Financial Health: {sv.get('financial_health_score', 0)}/100")
                print(f"   Statement Risk: {sv.get('statement_risk_level', 'Unknown')}")
                
                red_flags = sv.get('red_flags', [])
                print(f"\n🚨 Red Flags: {len(red_flags)}")
                if red_flags:
                    for flag in red_flags:
                        print(f"   ⚠️  {flag}")
                else:
                    print(f"   ✅ No red flags detected!")
            else:
                print(f"   Message: {sv.get('message', 'Processing failed')}")
            
            print(f"\n💡 Key Reasons:")
            for reason in result.get('reasons', [])[:3]:
                print(f"   - {reason}")
            
            print(f"\n📋 Recommendations:")
            for rec in result.get('recommendations', [])[:3]:
                print(f"   - {rec}")
            
            if 'ai_explanation' in result:
                print(f"\n🤖 AI Explanation:")
                print(f"   {result['ai_explanation']}")
            
            return result
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None


def show_usage():
    """Show usage instructions"""
    print("""
╔══════════════════════════════════════════════════════════════════╗
║          Unified API Test Script                                 ║
╚══════════════════════════════════════════════════════════════════╝

Usage:

  Test without bank statement:
    python test_api.py

  Test with bank statement:
    python test_api.py /path/to/statement.pdf

Examples:
    python test_api.py ~/Documents/hdfc_statement.pdf
    python test_api.py statement.pdf

Before running:
  1. Start Ollama: ollama serve
  2. Pull model: ollama pull llama3.2
  3. Start API: python enhanced_main.py
""")


def main():
    """Main test function"""
    print("\n" + "🚀 "*35)
    print("  Unified API Test Suite")
    print("🚀 "*35)
    
    # Check if API is healthy
    if not test_api_health():
        return
    
    # Test regular scoring
    result1 = test_regular_scoring()
    
    # Test with bank statement if provided
    if len(sys.argv) > 1:
        statement_path = sys.argv[1]
        result2 = test_with_bank_statement(statement_path)
    else:
        test_with_bank_statement(None)
    
    # Summary
    print_section("Summary")
    print("""
✅ Tests Completed!

Your API supports:
  1. Regular scoring (JSON) - Works! ✅
  2. Bank statement scoring (Form + File) - Ready! ✅

Next Steps:
  - Test with a real bank statement PDF
  - Integrate with your frontend
  - Deploy to production

For full documentation, see:
  - API_USAGE_EXAMPLES.md
  - UNIFIED_API_GUIDE.md
  - BANK_STATEMENT_GUIDE.md
""")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help', 'help']:
        show_usage()
    else:
        main()

