"""
Verification and Test Script for Smart Electricity Usage Analyzer
"""
import os
import sys

# Configure UTF-8 for console output on Windows if supported
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from app import app, load_data, perform_analysis, print_summary

def run_tests():
    print("Testing Smart Electricity Usage Analyzer...\n")
    
    # 1. Test data loading
    df = load_data()
    print(f"[OK] Loaded dataset successfully. Total records: {len(df)}")
    
    # 2. Test analysis & prediction
    results = perform_analysis(df)
    if results is None:
        print("[ERROR] Analysis returned None")
        sys.exit(1)
    print("[OK] Statistical analysis and ML prediction executed successfully.\n")
    
    # 3. Print output summary
    print_summary(results)
    
    # 4. Test Flask endpoints with test_client
    with app.test_client() as client:
        # Test Home route
        response = client.get("/")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        assert b"Smart Electricity Usage Analyzer" in response.data, "Dashboard title missing in HTML"
        print("\n[OK] Flask route GET / tested successfully (Status 200 OK, Dashboard rendered)")

    print("\nAll checks and tests passed successfully!")

if __name__ == "__main__":
    run_tests()