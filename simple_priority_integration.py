#!/usr/bin/env python3
"""
Simple Priority Integration System for KMRL
Integrates priority data across all systems
"""

import pandas as pd
import numpy as np
from datetime import datetime
import json

def integrate_priority_data():
    """Integrate priority data from all sources"""
    print("Integrating priority data across all systems...")
    
    try:
        # Load all datasets
        datasets = {}
        
        # Try realistic data first, fallback to training data
        files_to_load = [
            ('job_cards', ['realistic_job_cards.csv', 'maximo_job_cards.csv']),
            ('certificates', ['realistic_certificates.csv', 'fitness_certificates.csv']),
            ('mileage', ['realistic_mileage.csv', 'mileage_balancing.csv']),
            ('telemetry', ['realistic_telemetry.csv', 'iot_telemetry_data.csv']),
            ('stabling', ['realistic_stabling.csv', 'stabling_geometry.csv'])
        ]
        
        for name, file_options in files_to_load:
            loaded = False
            for file_path in file_options:
                try:
                    datasets[name] = pd.read_csv(file_path)
                    print(f"Loaded {name}: {len(datasets[name])} records from {file_path}")
                    loaded = True
                    break
                except FileNotFoundError:
                    continue
            
            if not loaded:
                print(f"Could not load {name} data")
        
        # Create integrated priority analysis
        train_ids = [f"CR{101+i:03d}" for i in range(24)]
        priority_data = []
        
        for train_id in train_ids:
            # Analyze job cards
            if 'job_cards' in datasets:
                train_jobs = datasets['job_cards'][datasets['job_cards']['Train_ID'] == train_id]
                critical_jobs = len(train_jobs[train_jobs['Priority'] == 'Critical']) if len(train_jobs) > 0 else 0
                total_jobs = len(train_jobs)
            else:
                critical_jobs = 0
                total_jobs = 0
            
            # Analyze certificates
            if 'certificates' in datasets:
                train_certs = datasets['certificates'][datasets['certificates']['Train_ID'] == train_id]
                expired_certs = len(train_certs[train_certs['Status'] == 'Expired']) if len(train_certs) > 0 else 0
                total_certs = len(train_certs)
            else:
                expired_certs = 0
                total_certs = 0
            
            # Analyze mileage/usage
            if 'mileage' in datasets:
                train_mileage = datasets['mileage'][datasets['mileage']['Train_ID'] == train_id]
                if len(train_mileage) > 0:
                    avg_usage = train_mileage['Average_Usage_Pct'].mean()
                    mileage_priority = train_mileage['Priority'].iloc[0] if 'Priority' in train_mileage.columns else 'Medium'
                else:
                    avg_usage = 50.0
                    mileage_priority = 'Medium'
            else:
                avg_usage = 50.0
                mileage_priority = 'Medium'
            
            # Analyze telemetry
            if 'telemetry' in datasets:
                train_telem = datasets['telemetry'][datasets['telemetry']['Train_ID'] == train_id]
                if len(train_telem) > 0:
                    health_score = train_telem['Health_Score'].mean()
                    temp = train_telem['Motor_Temperature_C'].mean()
                else:
                    health_score = 0.8
                    temp = 60.0
            else:
                health_score = 0.8
                temp = 60.0
            
            # Calculate overall priority score
            priority_score = 0
            
            # Job-based priority (40% weight)
            if critical_jobs > 0:
                priority_score += 40
            elif total_jobs > 15:  # High workload
                priority_score += 25
            elif total_jobs > 8:
                priority_score += 15
            
            # Certificate-based priority (30% weight)
            if expired_certs > 0:
                priority_score += 30
            elif total_certs > 0 and expired_certs == 0:
                priority_score += 5  # Good compliance
            
            # Usage-based priority (20% weight)
            if avg_usage > 70:
                priority_score += 20
            elif avg_usage > 50:
                priority_score += 10
            
            # Health-based priority (10% weight)
            if health_score < 0.7 or temp > 80:
                priority_score += 10
            
            # Determine overall priority
            if priority_score >= 60:
                overall_priority = 'Critical'
                action_required = 'Immediate'
            elif priority_score >= 40:
                overall_priority = 'High'
                action_required = 'Schedule Soon'
            elif priority_score >= 20:
                overall_priority = 'Medium'
                action_required = 'Monitor'
            else:
                overall_priority = 'Low'
                action_required = 'Normal Operations'
            
            priority_data.append({
                'Train_ID': train_id,
                'Overall_Priority': overall_priority,
                'Priority_Score': priority_score,
                'Action_Required': action_required,
                'Critical_Jobs': critical_jobs,
                'Total_Jobs': total_jobs,
                'Expired_Certificates': expired_certs,
                'Total_Certificates': total_certs,
                'Average_Usage_Pct': round(avg_usage, 1),
                'Health_Score': round(health_score, 3),
                'Temperature_C': round(temp, 1),
                'Analysis_Date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
        
        # Save integrated priority data
        priority_df = pd.DataFrame(priority_data)
        priority_df.to_csv('integrated_priority_data.csv', index=False)
        
        # Create priority summary
        summary = {
            'analysis_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total_trains': len(priority_data),
            'priority_distribution': priority_df['Overall_Priority'].value_counts().to_dict(),
            'high_priority_trains': len(priority_df[priority_df['Overall_Priority'].isin(['Critical', 'High'])]),
            'average_priority_score': round(priority_df['Priority_Score'].mean(), 1)
        }
        
        with open('priority_integration_summary.json', 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\nPriority integration complete!")
        print(f"Priority distribution: {summary['priority_distribution']}")
        print(f"High priority trains: {summary['high_priority_trains']}")
        print(f"Saved: integrated_priority_data.csv")
        return True
        
    except Exception as e:
        print(f"Priority integration failed: {e}")
        return False

if __name__ == "__main__":
    integrate_priority_data()