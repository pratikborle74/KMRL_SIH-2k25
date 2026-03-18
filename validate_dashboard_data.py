#!/usr/bin/env python3
"""
Data Validation Script for KMRL Dashboard
Tests that all CSV files load correctly and have expected columns
"""

import pandas as pd
import json
import os

def test_csv_loading(filename, expected_cols=None):
    """Test loading a CSV file and validate its structure"""
    print(f"\n--- Testing {filename} ---")
    
    try:
        if not os.path.exists(filename):
            print(f"❌ File not found: {filename}")
            return False
        
        df = pd.read_csv(filename)
        print(f"✅ File loaded successfully")
        print(f"📊 Shape: {df.shape}")
        print(f"🔍 Columns: {list(df.columns)}")
        
        if expected_cols:
            missing_cols = set(expected_cols) - set(df.columns)
            if missing_cols:
                print(f"⚠️  Missing expected columns: {missing_cols}")
            else:
                print("✅ All expected columns present")
        
        # Show sample data
        print("📝 Sample data:")
        print(df.head(2).to_string())
        
        return True
        
    except Exception as e:
        print(f"❌ Error loading {filename}: {e}")
        return False

def test_json_loading(filename):
    """Test loading a JSON file"""
    print(f"\n--- Testing {filename} ---")
    
    try:
        if not os.path.exists(filename):
            print(f"❌ File not found: {filename}")
            return False
        
        with open(filename, 'r') as f:
            data = json.load(f)
        
        print(f"✅ File loaded successfully")
        print(f"📊 Keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error loading {filename}: {e}")
        return False

def main():
    print("🚊 KMRL Dashboard Data Validation")
    print("=" * 50)
    
    # Test all CSV files used by the dashboard
    csv_tests = [
        ("maximo_job_cards.csv", ["Job_Number", "Status", "Priority", "Work_Type"]),
        ("fitness_certificates.csv", ["Train_ID", "Certificate_Type", "Issue_Date", "Expiry_Date"]),
        ("component_mileage.csv", ["Train_ID", "Bogie_Usage_Pct", "BrakePad_Usage_Pct"]),
        ("stabling_geometry.csv", ["Train_ID", "Current_Bay", "Current_Bay_Type", "Energy_Cost_Estimate"]),
    ]
    
    for filename, expected_cols in csv_tests:
        test_csv_loading(filename, expected_cols)
    
    # Test JSON files
    json_files = [
        "fleet_optimization_results.json",
        "ml_models_summary.json"
    ]
    
    for filename in json_files:
        test_json_loading(filename)
    
    print("\n" + "=" * 50)
    print("🏁 Validation Complete!")

if __name__ == "__main__":
    main()