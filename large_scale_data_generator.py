#!/usr/bin/env python3
"""
Large-Scale KMRL Data Generator for 98% ML Accuracy
Generates 100x larger datasets with enhanced patterns and realistic variations
"""

import pandas as pd
import numpy as np
from datetime import date, timedelta, datetime
import random
import json
import uuid
from scipy import stats
import itertools

# --- ENHANCED CONFIGURATION FOR LARGE-SCALE DATASETS ---
NUM_TRAINS = 24  # KMRL fleet size
FLEET_IDS = [f"CR{101 + i}" for i in range(NUM_TRAINS)]

# Extended simulation period for large datasets
START_DATE = date(2024, 1, 1)  # Full year of data
END_DATE = date(2025, 1, 31)   # Current + 1 month
SIMULATION_DAYS = (END_DATE - START_DATE).days  # ~395 days
CURRENT_DATE = date(2025, 1, 20)

# Multiple data generations for diversity
GENERATIONS_PER_TRAIN = 50  # Generate 50 different scenarios per train
TOTAL_RECORDS_TARGET = 50000  # Target for large dataset

# Enhanced departmental structure
DEPARTMENTS = ["Rolling_Stock", "Signalling", "Telecom", "Power_Supply", "Track_Maintenance"]
MAXIMO_WORK_ORDER_TYPES = [
    "PM-Bogie", "PM-Brake", "PM-HVAC", "PM-Doors", "PM-Traction", 
    "CM-Electrical", "CM-Mechanical", "CM-Electronics", "CM-Software",
    "Inspection-A", "Inspection-B", "Inspection-C", "Emergency-Repair",
    "Seasonal-Maintenance", "Compliance-Check"
]

# Enhanced cleaning operations
CLEANING_TYPES = [
    "Interior_Deep_Clean", "Exterior_Wash", "HVAC_Filter", "Window_Polish",
    "Seat_Sanitization", "Floor_Deep_Clean", "Graffiti_Removal", 
    "Disinfection_Spray", "LED_Light_Clean", "Driver_Cabin_Detail"
]

# Expanded stabling configuration
STABLING_BAYS = {
    "IBL_Maintenance": [f"IBL-{i}" for i in range(1, 12)],
    "Cleaning_Bays": [f"CB-{i}" for i in range(1, 8)],
    "Standard_Stabling": [f"SB-{i}" for i in range(1, 35)],
    "Standby_Ready": [f"RB-{i}" for i in range(1, 15)],
    "Heavy_Maintenance": [f"HM-{i}" for i in range(1, 6)]
}

# Enhanced branding contracts with more diversity
BRANDING_CONTRACTS_BASE = [
    {"Advertiser": "Lulu Mall", "Min_Hours_Daily": 15.5, "Contract_Value": 750000, "Penalty_Per_Hour": 2500},
    {"Advertiser": "MyG Digital", "Min_Hours_Daily": 14.0, "Contract_Value": 600000, "Penalty_Per_Hour": 2000},
    {"Advertiser": "Federal Bank", "Min_Hours_Daily": 16.0, "Contract_Value": 800000, "Penalty_Per_Hour": 3000},
    {"Advertiser": "Kerala Tourism", "Min_Hours_Daily": 13.5, "Contract_Value": 500000, "Penalty_Per_Hour": 1500},
    {"Advertiser": "Reliance Jio", "Min_Hours_Daily": 15.0, "Contract_Value": 700000, "Penalty_Per_Hour": 2200},
    {"Advertiser": "HDFC Bank", "Min_Hours_Daily": 14.5, "Contract_Value": 650000, "Penalty_Per_Hour": 2100},
    {"Advertiser": "Airtel", "Min_Hours_Daily": 16.5, "Contract_Value": 850000, "Penalty_Per_Hour": 3200},
    {"Advertiser": "Cochin Shipyard", "Min_Hours_Daily": 13.0, "Contract_Value": 480000, "Penalty_Per_Hour": 1400},
]

# Certificate validity periods (industry standards)
CERT_VALIDITY_DAYS = {
    "Rolling_Stock": 365,
    "Signalling": 180,
    "Telecom": 90,
    "Power_Supply": 270,
    "Track_Maintenance": 120
}

class LargeScaleDataGenerator:
    """Enhanced data generator for large-scale ML training"""
    
    def __init__(self):
        self.generated_data = {}
        self.patterns = self._create_realistic_patterns()
        
    def _create_realistic_patterns(self):
        """Create realistic operational patterns for data generation"""
        patterns = {
            'seasonal_usage': {
                'monsoon_months': [6, 7, 8, 9],  # Higher maintenance needs
                'peak_months': [11, 12, 1, 2],   # Higher service requirements
                'maintenance_months': [3, 4, 5, 10]  # Planned maintenance windows
            },
            'daily_patterns': {
                'peak_hours': list(range(7, 10)) + list(range(17, 20)),
                'off_peak_hours': list(range(23, 6)) + list(range(10, 17)),
                'maintenance_hours': list(range(0, 5))
            },
            'failure_correlations': {
                'high_usage_failures': ['Motor_Temperature', 'Brake_Wear', 'Bogie_Stress'],
                'weather_failures': ['Door_Mechanism', 'HVAC_System', 'Electrical_Systems'],
                'age_failures': ['Software_Glitches', 'Sensor_Degradation', 'Component_Fatigue']
            }
        }
        return patterns
        
    def generate_large_fitness_certificates(self):
        """Generate large-scale fitness certificates with realistic patterns"""
        print("📋 Generating large-scale fitness certificates...")
        
        certificates = []
        
        # Generate certificates for extended time period
        for train_id in FLEET_IDS:
            for dept in DEPARTMENTS:
                # Generate multiple certificate cycles over the simulation period
                validity_days = CERT_VALIDITY_DAYS[dept]
                
                # Calculate how many certificate cycles would occur
                cycles = (SIMULATION_DAYS // validity_days) + 2
                
                for cycle in range(cycles):
                    base_issue_date = START_DATE + timedelta(days=cycle * validity_days)
                    
                    # Add some randomization to issue dates
                    issue_date = base_issue_date + timedelta(days=random.randint(-10, 10))
                    expiry_date = issue_date + timedelta(days=validity_days)
                    
                    # Determine status based on current date and expiry
                    days_to_expiry = (expiry_date - CURRENT_DATE).days
                    
                    if days_to_expiry < -30:
                        continue  # Skip very old expired certificates
                    elif days_to_expiry < 0:
                        status = "Expired"
                        priority = "Critical"
                    elif days_to_expiry < 15:
                        status = "Renewal_In_Progress"
                        priority = "High"
                    elif days_to_expiry < 30:
                        status = "Valid"
                        priority = "Medium"
                    else:
                        status = "Valid"
                        priority = "Low"
                    
                    # Add some pending certificates for realism
                    if random.random() < 0.02:  # 2% pending
                        status = "Pending"
                        priority = "Critical"
                    
                    certificates.append({
                        "Certificate_ID": f"CERT-{dept[:3].upper()}-{train_id}-{cycle:03d}-{uuid.uuid4().hex[:6]}",
                        "Train_ID": train_id,
                        "Department": dept,
                        "Issue_Date": issue_date.strftime("%Y-%m-%d") if issue_date <= CURRENT_DATE else None,
                        "Expiry_Date": expiry_date.strftime("%Y-%m-%d"),
                        "Validity_Days": validity_days,
                        "Status": status,
                        "Inspector": f"{dept}_Inspector_{random.randint(1, 15)}",
                        "Priority": priority,
                        "Inspection_Type": self._get_inspection_type(dept),
                        "Cycle_Number": cycle,
                        "Compliance_Score": random.uniform(85, 99) if status == "Valid" else random.uniform(60, 85),
                        "Notes": f"Cycle {cycle} certificate for {dept.lower()} systems"
                    })
        
        print(f"✅ Generated {len(certificates)} fitness certificates")
        return pd.DataFrame(certificates)
    
    def _get_inspection_type(self, dept):
        """Get appropriate inspection type for department"""
        inspection_types = {
            "Rolling_Stock": "Annual_Comprehensive",
            "Signalling": "Semi_Annual_Systems",
            "Telecom": "Quarterly_Network",
            "Power_Supply": "Triannual_Power",
            "Track_Maintenance": "Quarterly_Track"
        }
        return inspection_types.get(dept, "Standard_Inspection")
    
    def generate_large_maximo_job_cards(self):
        """Generate large-scale Maximo job cards with realistic patterns"""
        print("🔧 Generating large-scale Maximo job cards...")
        
        job_cards = []
        
        # Generate historical job cards over entire simulation period
        for current_date in pd.date_range(START_DATE, CURRENT_DATE, freq='D'):
            # Vary job creation rate by season and day of week
            base_jobs_per_day = 3
            
            # Seasonal variations
            month = current_date.month
            if month in self.patterns['seasonal_usage']['monsoon_months']:
                job_multiplier = 1.5  # More maintenance needed
            elif month in self.patterns['seasonal_usage']['peak_months']:
                job_multiplier = 1.3  # Higher usage wear
            else:
                job_multiplier = 1.0
            
            # Weekend effect (less jobs created on weekends)
            if current_date.weekday() >= 5:
                job_multiplier *= 0.7
            
            daily_jobs = int(base_jobs_per_day * job_multiplier * random.uniform(0.5, 1.8))
            
            for _ in range(daily_jobs):
                train_id = random.choice(FLEET_IDS)
                work_type = random.choice(MAXIMO_WORK_ORDER_TYPES)
                
                # Realistic priority distribution
                priority_weights = [0.05, 0.15, 0.35, 0.45]  # Critical, High, Medium, Low
                priority = np.random.choice(["Critical", "High", "Medium", "Low"], p=priority_weights)
                
                # Status based on age and priority
                age_days = (CURRENT_DATE - current_date.date()).days
                status = self._determine_job_status(priority, age_days)
                
                # Enhanced estimated hours with work type patterns
                est_hours = self._calculate_realistic_hours(work_type, priority)
                
                job_cards.append({
                    "Work_Order_ID": f"WO-{uuid.uuid4().hex[:8].upper()}",
                    "Job_Number": f"JOB-{current_date.strftime('%Y%m%d')}-{random.randint(1000, 9999)}",
                    "Train_ID": train_id,
                    "Work_Type": work_type,
                    "Description": self._generate_realistic_description(work_type, train_id),
                    "Priority": priority,
                    "Status": status,
                    "Created_Date": current_date.strftime("%Y-%m-%d"),
                    "Due_Date": (current_date + timedelta(days=self._calculate_due_days(priority))).strftime("%Y-%m-%d"),
                    "Estimated_Hours": est_hours,
                    "Actual_Hours": self._calculate_actual_hours(est_hours, status),
                    "Assigned_Technician": f"Tech_{random.randint(1, 30)}",
                    "Department": self._assign_department(work_type),
                    "Cost_Estimate": est_hours * random.randint(75, 200),
                    "Parts_Cost": random.randint(500, 5000) if "CM-" in work_type else random.randint(100, 1000),
                    "Urgency_Score": self._calculate_urgency_score(priority, age_days),
                    "Completion_Rate": self._calculate_completion_rate(status, age_days),
                    "Notes": f"Generated on {current_date.strftime('%Y-%m-%d')} - {work_type} maintenance"
                })
        
        print(f"✅ Generated {len(job_cards)} Maximo job cards")
        return pd.DataFrame(job_cards)
    
    def _determine_job_status(self, priority, age_days):
        """Determine realistic job status based on priority and age"""
        if priority == "Critical":
            if age_days <= 1:
                return "Open"
            elif age_days <= 3:
                return "In_Progress"
            else:
                return "Closed"
        elif priority == "High":
            if age_days <= 2:
                return random.choice(["Open", "In_Progress"])
            elif age_days <= 7:
                return random.choice(["In_Progress", "Closed"])
            else:
                return "Closed"
        elif priority == "Medium":
            if age_days <= 5:
                return random.choice(["Open", "In_Progress"])
            elif age_days <= 14:
                return random.choice(["In_Progress", "Closed", "On_Hold"])
            else:
                return random.choice(["Closed", "On_Hold"])
        else:  # Low priority
            if age_days <= 10:
                return random.choice(["Open", "In_Progress", "On_Hold"])
            else:
                return random.choice(["Closed", "On_Hold", "Cancelled"])
    
    def _calculate_realistic_hours(self, work_type, priority):
        """Calculate realistic estimated hours based on work type and priority"""
        base_hours = {
            "PM-Bogie": (8, 16), "PM-Brake": (4, 8), "PM-HVAC": (6, 12),
            "PM-Doors": (3, 6), "PM-Traction": (10, 20), "CM-Electrical": (2, 24),
            "CM-Mechanical": (4, 20), "CM-Electronics": (3, 12), "CM-Software": (1, 8),
            "Inspection-A": (6, 10), "Inspection-B": (12, 20), "Inspection-C": (20, 32),
            "Emergency-Repair": (1, 48), "Seasonal-Maintenance": (16, 40), "Compliance-Check": (2, 6)
        }
        
        min_hours, max_hours = base_hours.get(work_type, (2, 8))
        
        # Priority affects complexity
        priority_multiplier = {"Critical": 1.5, "High": 1.2, "Medium": 1.0, "Low": 0.8}
        multiplier = priority_multiplier.get(priority, 1.0)
        
        return int((random.uniform(min_hours, max_hours)) * multiplier)
    
    def _generate_realistic_description(self, work_type, train_id):
        """Generate realistic job descriptions"""
        descriptions = {
            "PM-Bogie": [f"Scheduled bogie maintenance for {train_id}", f"Bogie bearing inspection and lubrication - {train_id}"],
            "PM-Brake": [f"Brake system preventive maintenance - {train_id}", f"Brake pad inspection and replacement - {train_id}"],
            "CM-Electrical": [f"Electrical system corrective maintenance - {train_id}", f"Power supply issue resolution - {train_id}"],
            "Emergency-Repair": [f"Emergency repair required - {train_id}", f"Urgent maintenance intervention - {train_id}"]
        }
        
        return random.choice(descriptions.get(work_type, [f"{work_type.replace('-', ' ')} for {train_id}"]))
    
    def _assign_department(self, work_type):
        """Assign appropriate department based on work type"""
        dept_mapping = {
            "PM-Bogie": "Mechanical", "PM-Brake": "Mechanical", "PM-HVAC": "Electrical",
            "PM-Doors": "Mechanical", "PM-Traction": "Electrical", "CM-Electrical": "Electrical",
            "CM-Mechanical": "Mechanical", "CM-Electronics": "Electronics", "CM-Software": "IT",
            "Emergency-Repair": "Emergency_Response", "Compliance-Check": "Quality_Assurance"
        }
        return dept_mapping.get(work_type, "Maintenance")
    
    def _calculate_due_days(self, priority):
        """Calculate realistic due dates based on priority"""
        due_days = {"Critical": random.randint(1, 2), "High": random.randint(3, 7), 
                   "Medium": random.randint(7, 21), "Low": random.randint(14, 45)}
        return due_days.get(priority, 14)
    
    def _calculate_actual_hours(self, estimated_hours, status):
        """Calculate actual hours based on status and estimation accuracy"""
        if status in ["Open", "In_Progress"]:
            return None  # Not completed yet
        elif status == "Closed":
            # Actual hours typically vary from estimate
            variance = random.uniform(0.8, 1.3)
            return round(estimated_hours * variance, 1)
        else:
            return None
    
    def _calculate_urgency_score(self, priority, age_days):
        """Calculate urgency score based on priority and age"""
        base_scores = {"Critical": 90, "High": 70, "Medium": 50, "Low": 30}
        base_score = base_scores.get(priority, 50)
        
        # Increase urgency with age for open items
        age_factor = min(20, age_days * 2)
        return min(100, base_score + age_factor)
    
    def _calculate_completion_rate(self, status, age_days):
        """Calculate completion rate for performance metrics"""
        if status == "Closed":
            return 100.0
        elif status == "In_Progress":
            return random.uniform(20, 80)
        elif status == "On_Hold":
            return random.uniform(10, 30)
        else:
            return 0.0
    
    def generate_comprehensive_telemetry(self):
        """Generate comprehensive IoT telemetry data with realistic sensor patterns"""
        print("📡 Generating comprehensive IoT telemetry data...")
        
        telemetry_records = []
        
        # Generate telemetry for each train over extended period
        for train_id in FLEET_IDS:
            # Create unique baseline characteristics for each train
            train_age_months = random.randint(6, 60)  # 6 months to 5 years
            train_usage_intensity = random.uniform(0.7, 1.3)  # Usage intensity factor
            
            # Generate daily telemetry records
            for current_date in pd.date_range(START_DATE, CURRENT_DATE, freq='D'):
                # Skip some days for maintenance/non-operation
                if random.random() < 0.05:  # 5% downtime
                    continue
                
                # Generate multiple readings per day (hourly during operation)
                operating_hours = random.randint(14, 18)  # 14-18 hours operation
                
                for hour in range(operating_hours):
                    timestamp = current_date + pd.Timedelta(hours=hour)
                    
                    # Generate realistic sensor readings with patterns
                    base_temp = 45 + train_age_months * 0.5  # Older trains run hotter
                    motor_temp = base_temp + random.normalvariate(0, 8)  # Normal variation
                    
                    # Seasonal effects on temperature
                    month = current_date.month
                    if month in [5, 6, 7, 8]:  # Hot months
                        motor_temp += random.uniform(5, 15)
                    elif month in [11, 12, 1, 2]:  # Cool months
                        motor_temp -= random.uniform(2, 8)
                    
                    # Current follows temperature with some correlation
                    base_current = 180 + (motor_temp - 50) * 2
                    motor_current = max(120, base_current + random.normalvariate(0, 25))
                    
                    # Brake pressure varies with usage
                    brake_pressure = random.uniform(4.5, 6.5) + random.normalvariate(0, 0.5)
                    
                    # HVAC power correlates with external temperature
                    hvac_base = 8 if month in [5, 6, 7, 8] else 4  # Higher in summer
                    hvac_power = hvac_base + random.uniform(2, 8) + random.normalvariate(0, 1.5)
                    
                    # Vibration increases with age and usage
                    vibration_base = 2.0 + train_age_months * 0.1 + train_usage_intensity * 0.5
                    vibration = max(1.0, vibration_base + random.normalvariate(0, 0.8))
                    
                    # Oil temperature follows motor temperature
                    oil_temp = motor_temp * 0.85 + random.normalvariate(0, 5)
                    
                    # Health score calculation (inverse of wear indicators)
                    health_components = [
                        max(0, 100 - max(0, motor_temp - 65) * 2),  # Temperature stress
                        max(0, 100 - max(0, motor_current - 220) * 1),  # Current stress
                        max(0, 100 - max(0, vibration - 3.0) * 10),  # Vibration stress
                        max(0, 100 - train_age_months * 1.2)  # Age factor
                    ]
                    health_score = np.mean(health_components) / 100
                    
                    telemetry_records.append({
                        "Train_ID": train_id,
                        "Timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                        "Date": current_date.strftime("%Y-%m-%d"),
                        "Hour": hour,
                        "Motor_Temperature_C": round(max(25, min(120, motor_temp)), 1),
                        "Motor_Current_A": round(max(100, min(350, motor_current)), 1),
                        "Brake_Pressure_Bar": round(max(3.0, min(8.0, brake_pressure)), 2),
                        "HVAC_Power_kW": round(max(2, min(25, hvac_power)), 1),
                        "Vibration_Level": round(max(1.0, min(10.0, vibration)), 2),
                        "Oil_Temperature_C": round(max(20, min(100, oil_temp)), 1),
                        "Health_Score": round(max(0.3, min(1.0, health_score)), 3),
                        "Train_Age_Months": train_age_months,
                        "Usage_Intensity": round(train_usage_intensity, 2),
                        "Operating_Hour": hour,
                        "Season": "Summer" if month in [3,4,5,6] else "Winter" if month in [11,12,1,2] else "Monsoon"
                    })
        
        print(f"✅ Generated {len(telemetry_records)} telemetry records")
        return pd.DataFrame(telemetry_records)
    
    def generate_all_large_datasets(self):
        """Generate all large-scale datasets"""
        print("🚀 Starting large-scale data generation for 98% ML accuracy...")
        print(f"📊 Target simulation period: {SIMULATION_DAYS} days")
        print(f"🚆 Fleet size: {NUM_TRAINS} trains")
        
        # Generate all datasets
        datasets = {}
        
        # 1. Fitness Certificates
        datasets['fitness_certificates'] = self.generate_large_fitness_certificates()
        
        # 2. Maximo Job Cards  
        datasets['maximo_job_cards'] = self.generate_large_maximo_job_cards()
        
        # 3. IoT Telemetry
        datasets['iot_telemetry'] = self.generate_comprehensive_telemetry()
        
        # 4. Enhanced datasets (using existing logic but scaled up)
        datasets.update(self._generate_remaining_datasets())
        
        # Save all datasets
        for name, df in datasets.items():
            filename = f"{name}.csv"
            df.to_csv(filename, index=False)
            print(f"💾 Saved {filename} ({len(df)} records)")
        
        # Generate summary
        self._generate_data_summary(datasets)
        
        print("🎉 Large-scale data generation completed!")
        return datasets
    
    def _generate_remaining_datasets(self):
        """Generate remaining datasets with enhanced scale"""
        datasets = {}
        
        # Enhanced mileage balancing
        datasets['mileage_balancing'] = self._generate_enhanced_mileage()
        datasets['branding_priorities'] = self._generate_enhanced_branding()
        datasets['cleaning_detailing_schedule'] = self._generate_enhanced_cleaning()
        datasets['stabling_geometry'] = self._generate_enhanced_stabling()
        
        return datasets
    
    def _generate_enhanced_mileage(self):
        """Generate enhanced mileage data with realistic usage patterns"""
        mileage_data = []
        
        for train_id in FLEET_IDS:
            # Generate historical mileage tracking
            for days_ago in range(0, min(365, SIMULATION_DAYS), 7):  # Weekly snapshots
                current_date = CURRENT_DATE - timedelta(days=days_ago)
                
                # Age-based wear progression
                train_age_days = (current_date - START_DATE).days
                age_factor = train_age_days / 365.0  # Years of operation
                
                # Component usage percentages with realistic correlations
                base_usage = 20 + age_factor * 15  # Base wear increases with age
                
                # Realistic component wear correlations
                bogie_usage = base_usage + random.uniform(-10, 15)
                brake_usage = base_usage + random.uniform(-8, 12)  # Related to bogie
                hvac_usage = base_usage + random.uniform(-15, 10)  # Less correlated
                motor_usage = base_usage + random.uniform(-5, 20)  # Highly used
                
                # Ensure realistic ranges
                bogie_usage = max(5, min(95, bogie_usage))
                brake_usage = max(5, min(95, brake_usage))
                hvac_usage = max(5, min(95, hvac_usage))
                motor_usage = max(5, min(95, motor_usage))
                
                avg_usage = np.mean([bogie_usage, brake_usage, hvac_usage, motor_usage])
                
                # Determine critical components
                critical_components = []
                if bogie_usage > 80: critical_components.append("Bogie_Mileage")
                if brake_usage > 80: critical_components.append("BrakePad_Mileage")
                if hvac_usage > 80: critical_components.append("HVAC_Hours")
                if motor_usage > 80: critical_components.append("Motor_Hours")
                
                # Priority and recommendations
                if avg_usage > 85:
                    priority = "Critical"
                    recommendation = "Immediate_Maintenance"
                elif avg_usage > 70:
                    priority = "High"
                    recommendation = "Schedule_Maintenance"
                elif avg_usage > 40:
                    priority = "Medium"
                    recommendation = "Monitor_Closely"
                else:
                    priority = "Low"
                    recommendation = "Continue_Operation"
                
                mileage_data.append({
                    "Train_ID": train_id,
                    "Date": current_date.strftime("%Y-%m-%d"),
                    "Bogie_Usage_Pct": round(bogie_usage, 1),
                    "BrakePad_Usage_Pct": round(brake_usage, 1),
                    "HVAC_Usage_Pct": round(hvac_usage, 1),
                    "Motor_Usage_Pct": round(motor_usage, 1),
                    "Average_Usage_Pct": round(avg_usage, 1),
                    "Critical_Components": ",".join(critical_components) if critical_components else "",
                    "Priority": priority,
                    "Recommendation": recommendation,
                    "Balancing_Score": round(100 - avg_usage, 1),
                    "Age_Factor": round(age_factor, 2),
                    "Maintenance_Due": avg_usage > 75,
                    "Notes": f"Week {days_ago//7} snapshot - {len(critical_components)} critical components"
                })
        
        return pd.DataFrame(mileage_data)
    
    def _generate_enhanced_branding(self):
        """Generate enhanced branding data"""
        branding_data = []
        
        # Assign contracts to different trains
        contract_assignments = {}
        available_trains = FLEET_IDS.copy()
        
        for i, contract_base in enumerate(BRANDING_CONTRACTS_BASE):
            if available_trains:
                train_id = random.choice(available_trains)
                available_trains.remove(train_id)
                
                contract_assignments[train_id] = {
                    "Contract_ID": f"BRD-{i+1:03d}",
                    **contract_base
                }
        
        # Generate historical performance data
        for train_id, contract in contract_assignments.items():
            for current_date in pd.date_range(START_DATE, CURRENT_DATE, freq='D'):
                # Realistic service hours with variations
                base_service_hours = 16.5  # Standard KMRL operation
                
                # Day of week effects
                if current_date.weekday() == 6:  # Sunday
                    service_multiplier = 0.8
                elif current_date.weekday() >= 5:  # Weekend
                    service_multiplier = 0.9
                else:
                    service_multiplier = 1.0
                
                # Random operational variations
                operational_efficiency = random.uniform(0.85, 1.05)
                actual_hours = base_service_hours * service_multiplier * operational_efficiency
                
                # Calculate compliance
                required_hours = contract["Min_Hours_Daily"]
                shortfall = max(0, required_hours - actual_hours)
                penalty = shortfall * contract["Penalty_Per_Hour"]
                compliance_pct = min(100, (actual_hours / required_hours) * 100)
                
                branding_data.append({
                    "Contract_ID": contract["Contract_ID"],
                    "Train_ID": train_id,
                    "Advertiser": contract["Advertiser"],
                    "Date": current_date.strftime("%Y-%m-%d"),
                    "Required_Hours": required_hours,
                    "Actual_Service_Hours": round(actual_hours, 1),
                    "Shortfall_Hours": round(shortfall, 1),
                    "Penalty_Incurred": round(penalty, 0),
                    "Compliance_Percentage": round(compliance_pct, 1),
                    "Contract_Value": contract["Contract_Value"],
                    "Priority": "Critical" if compliance_pct < 90 else "Medium" if compliance_pct < 95 else "Low",
                    "Revenue_Impact": round(penalty, 0),
                    "Day_Of_Week": current_date.strftime("%A"),
                    "Month": current_date.strftime("%B"),
                    "Notes": f"Daily tracking for {contract['Advertiser']} contract"
                })
        
        return pd.DataFrame(branding_data)
    
    def _generate_enhanced_cleaning(self):
        """Generate enhanced cleaning schedule data"""
        cleaning_data = []
        
        for train_id in FLEET_IDS:
            for current_date in pd.date_range(START_DATE, CURRENT_DATE, freq='D'):
                # Not every train gets cleaned every day
                if random.random() < 0.3:  # 30% chance of cleaning per day
                    continue
                
                # Random cleaning types
                num_cleaning_types = random.randint(1, 3)
                selected_types = random.sample(CLEANING_TYPES, num_cleaning_types)
                
                for cleaning_type in selected_types:
                    # Realistic duration and costs
                    duration_mapping = {
                        "Interior_Deep_Clean": (120, 180),
                        "Exterior_Wash": (45, 75),
                        "HVAC_Filter": (60, 90),
                        "Window_Polish": (30, 60),
                        "Seat_Sanitization": (90, 120),
                        "Floor_Deep_Clean": (60, 120),
                        "Graffiti_Removal": (30, 180),
                        "Disinfection_Spray": (20, 40),
                        "LED_Light_Clean": (45, 60),
                        "Driver_Cabin_Detail": (30, 45)
                    }
                    
                    min_dur, max_dur = duration_mapping.get(cleaning_type, (30, 120))
                    duration = random.randint(min_dur, max_dur)
                    
                    cleaning_data.append({
                        "Train_ID": train_id,
                        "Date": current_date.strftime("%Y-%m-%d"),
                        "Cleaning_Type": cleaning_type,
                        "Duration_Minutes": duration,
                        "Cost": random.randint(500, 2000),
                        "Staff_Assigned": random.randint(2, 6),
                        "Priority": random.choice(["High", "Medium", "Low"]),
                        "Completion_Status": random.choice(["Completed", "In_Progress", "Scheduled"]),
                        "Quality_Score": random.uniform(85, 98),
                        "Location": random.choice(["Depot_A", "Depot_B", "Terminal_Station"]),
                        "Shift": random.choice(["Morning", "Evening", "Night"]),
                        "Notes": f"{cleaning_type.replace('_', ' ')} performed on {train_id}"
                    })
        
        return pd.DataFrame(cleaning_data)
    
    def _generate_enhanced_stabling(self):
        """Generate enhanced stabling geometry data"""
        stabling_data = []
        
        # Assign trains to bays with realistic distributions
        all_bays = []
        for bay_type, bays in STABLING_BAYS.items():
            for bay in bays:
                all_bays.append({"bay": bay, "type": bay_type})
        
        # Current assignments
        assigned_bays = random.sample(all_bays, NUM_TRAINS)
        
        for i, train_id in enumerate(FLEET_IDS):
            bay_info = assigned_bays[i]
            current_bay = bay_info["bay"]
            bay_type = bay_info["type"]
            
            # Generate realistic stabling metrics
            accessibility_score = {
                "IBL_Maintenance": random.randint(4, 5),
                "Cleaning_Bays": random.randint(4, 5),
                "Standard_Stabling": random.randint(2, 3),
                "Standby_Ready": random.randint(4, 5),
                "Heavy_Maintenance": random.randint(3, 4)
            }.get(bay_type, 3)
            
            exit_time = {
                "IBL_Maintenance": random.randint(15, 30),
                "Cleaning_Bays": random.randint(10, 20),
                "Standard_Stabling": random.randint(20, 40),
                "Standby_Ready": random.randint(5, 15),
                "Heavy_Maintenance": random.randint(25, 45)
            }.get(bay_type, 25)
            
            shunting_moves = random.randint(0, 4)
            shunting_time = shunting_moves * random.randint(8, 15)
            
            # Energy cost estimation
            base_cost = 200
            energy_cost = base_cost + shunting_moves * 150 + exit_time * 10
            
            # Tomorrow's status prediction
            tomorrow_status = random.choice([
                "Service", "Maintenance", "Cleaning", "Standby", "Testing"
            ])
            
            # Reallocation need assessment
            optimal_bay_type = {
                "Service": "Standby_Ready",
                "Maintenance": "IBL_Maintenance", 
                "Cleaning": "Cleaning_Bays",
                "Standby": "Standard_Stabling",
                "Testing": "IBL_Maintenance"
            }.get(tomorrow_status, bay_type)
            
            needs_reallocation = optimal_bay_type != bay_type
            priority = "High" if needs_reallocation and shunting_moves > 2 else "Medium" if needs_reallocation else "Low"
            
            stabling_data.append({
                "Train_ID": train_id,
                "Current_Bay": current_bay,
                "Current_Bay_Type": bay_type,
                "Accessibility_Score": accessibility_score,
                "Exit_Time_Minutes": exit_time,
                "Shunting_Moves_Required": shunting_moves,
                "Shunting_Time_Minutes": shunting_time,
                "Tomorrow_Status": tomorrow_status,
                "Optimal_Bay_Type": optimal_bay_type,
                "Needs_Reallocation": needs_reallocation,
                "Reallocation_Priority": priority,
                "Energy_Cost_Estimate": energy_cost,
                "Capacity_Utilization": random.uniform(0.7, 0.95),
                "Safety_Score": random.uniform(85, 98),
                "Distance_To_Workshop": random.randint(50, 500),
                "Notes": f"Currently in {current_bay}, optimized for {tomorrow_status}"
            })
        
        return pd.DataFrame(stabling_data)
    
    def _generate_data_summary(self, datasets):
        """Generate comprehensive data summary for ML training"""
        summary = {
            "generation_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "simulation_period": {
                "start_date": START_DATE.strftime("%Y-%m-%d"),
                "end_date": END_DATE.strftime("%Y-%m-%d"),
                "total_days": SIMULATION_DAYS
            },
            "fleet_configuration": {
                "total_trains": NUM_TRAINS,
                "train_ids": FLEET_IDS
            },
            "dataset_statistics": {}
        }
        
        for name, df in datasets.items():
            summary["dataset_statistics"][name] = {
                "total_records": len(df),
                "columns": list(df.columns),
                "date_range": {
                    "start": df['Date'].min() if 'Date' in df.columns else "N/A",
                    "end": df['Date'].max() if 'Date' in df.columns else "N/A"
                } if 'Date' in df.columns else "No date column",
                "unique_trains": df['Train_ID'].nunique() if 'Train_ID' in df.columns else "N/A",
                "memory_usage_mb": round(df.memory_usage(deep=True).sum() / 1024 / 1024, 2)
            }
        
        # Save summary
        with open('large_scale_data_summary.json', 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"📋 Data generation summary saved to 'large_scale_data_summary.json'")
        
        # Print quick stats
        total_records = sum(len(df) for df in datasets.values())
        print(f"\n📊 LARGE-SCALE DATA GENERATION SUMMARY:")
        print(f"   📈 Total records generated: {total_records:,}")
        print(f"   📅 Simulation period: {SIMULATION_DAYS} days")
        print(f"   🚆 Fleet coverage: {NUM_TRAINS} trains")
        print(f"   💾 Total datasets: {len(datasets)}")

def main():
    """Main function to generate large-scale datasets"""
    print("🚀 KMRL Large-Scale Data Generator for 98% ML Accuracy")
    print("=" * 60)
    
    generator = LargeScaleDataGenerator()
    datasets = generator.generate_all_large_datasets()
    
    print("\n🎯 Large-scale datasets ready for advanced ML training!")
    print("Next step: Run enhanced ML training script")

if __name__ == "__main__":
    main()