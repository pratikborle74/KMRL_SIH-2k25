#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ML Models Sanity Check - Verifies the health of the ML models and system components
"""

import os
import json
import pandas as pd
import numpy as np
import sys
import datetime
from pathlib import Path

def check_file_exists(filename):
    """Check if a file exists and return its size"""
    path = Path(filename)
    if path.exists():
        return True, path.stat().st_size
    return False, 0

def validate_csv_file(filename, required_columns=None):
    """Validate a CSV file's structure"""
    exists, size = check_file_exists(filename)
    if not exists:
        return False, f"File {filename} does not exist"
    
    if size == 0:
        return False, f"File {filename} is empty"
    
    try:
        df = pd.read_csv(filename)
        if required_columns:
            missing_cols = [col for col in required_columns if col not in df.columns]
            if missing_cols:
                return False, f"File {filename} is missing columns: {', '.join(missing_cols)}"
        
        return True, f"File {filename} is valid ({len(df)} rows, {len(df.columns)} columns)"
    except Exception as e:
        return False, f"Error validating {filename}: {str(e)}"

def validate_json_file(filename, required_keys=None):
    """Validate a JSON file's structure"""
    exists, size = check_file_exists(filename)
    if not exists:
        return False, f"File {filename} does not exist"
    
    if size == 0:
        return False, f"File {filename} is empty"
    
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        
        if required_keys:
            missing_keys = [key for key in required_keys if key not in data]
            if missing_keys:
                return False, f"File {filename} is missing keys: {', '.join(missing_keys)}"
        
        return True, f"File {filename} is valid JSON"
    except Exception as e:
        return False, f"Error validating {filename}: {str(e)}"

def run_health_check():
    """Run a comprehensive health check on ML models and system components"""
    check_results = {
        "timestamp": datetime.datetime.now().isoformat(),
        "system_health": True,
        "checks": []
    }
    
    # Check required data files
    data_files = {
        "fitness_certificates.csv": ["Certificate_ID", "Train_ID", "Status"],
        "maximo_job_cards.csv": ["Work_Order_ID", "Priority", "Status"],
        "stabling_geometry.csv": ["Train_ID", "Current_Bay"],
        "mileage_balancing.csv": ["Train_ID", "Current_Mileage"],
        "workers.csv": ["Worker_ID", "Availability"],
        "iot_telemetry_data.csv": ["Train_ID", "Timestamp", "Sensor_Value"],
    }
    
    for filename, required_cols in data_files.items():
        valid, message = validate_csv_file(filename, required_cols)
        check_results["checks"].append({
            "component": f"Data file: {filename}",
            "status": "PASS" if valid else "FAIL",
            "message": message
        })
        if not valid:
            check_results["system_health"] = False
    
    # Check optimization results
    valid, message = validate_json_file('intelligent_optimization_results.json', 
                                       ["optimization_summary", "train_recommendations", "ml_insights"])
    check_results["checks"].append({
        "component": "Optimization results",
        "status": "PASS" if valid else "FAIL",
        "message": message
    })
    if not valid:
        check_results["system_health"] = False
    
    # Check demo data files
    demo_files = [
        "demo_certificates.csv",
        "demo_job_cards.csv",
        "demo_telemetry.csv",
        "demo_stabling_geometry.csv",
        "realistic_mileage.csv",
    ]
    
    for filename in demo_files:
        valid, message = validate_csv_file(filename)
        check_results["checks"].append({
            "component": f"Demo file: {filename}",
            "status": "PASS" if valid else "WARNING",
            "message": message
        })
        # Demo files are not critical, so we don't set system_health to False
    
    # Check Python modules
    modules = [
        "advanced_ml_models.py",
        "enhanced_data_generator.py",
        "intelligent_optimization_engine.py",
        "simple_priority_integration.py",
    ]
    
    for module in modules:
        exists, size = check_file_exists(module)
        check_results["checks"].append({
            "component": f"Module: {module}",
            "status": "PASS" if exists else "FAIL",
            "message": f"Module {module} {'exists' if exists else 'is missing'}"
        })
        if not exists:
            check_results["system_health"] = False
    
    # Save health check results
    with open('system_health_check.json', 'w') as f:
        json.dump(check_results, f, indent=4)
    
    # Print summary to console
    passed = sum(1 for check in check_results["checks"] if check["status"] == "PASS")
    total = len(check_results["checks"])
    print(f"Health Check Complete: {passed}/{total} checks passed")
    print(f"System health: {'HEALTHY' if check_results['system_health'] else 'UNHEALTHY'}")
    
    # Return success/failure for system process
    return check_results["system_health"]

if __name__ == "__main__":
    success = run_health_check()
    sys.exit(0 if success else 1)