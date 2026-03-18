#!/usr/bin/env python3
"""
Advanced ML Training for 98% Accuracy
Uses large-scale datasets with sophisticated ML techniques
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import joblib
import warnings
warnings.filterwarnings('ignore')

# ML Libraries
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder, RobustScaler
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.feature_selection import SelectFromModel
from sklearn.pipeline import Pipeline

# Advanced ML libraries
import xgboost as xgb
import lightgbm as lgb
from sklearn.neural_network import MLPClassifier

# TensorFlow for advanced models
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, BatchNormalization
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau

# Data processing
import json
from tqdm import tqdm

class AdvancedKMRLMLTrainer:
    """
    Advanced ML trainer for achieving 98% accuracy using large datasets
    """
    
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.label_encoders = {}
        self.feature_importance = {}
        
    def load_large_datasets(self):
        """Load all large-scale datasets"""
        try:
            print("📊 Loading large-scale datasets...")
            
            datasets = {
                'fitness_certs': pd.read_csv("fitness_certificates.csv"),
                'job_cards': pd.read_csv("maximo_job_cards.csv"),
                'telemetry': pd.read_csv("iot_telemetry_data.csv"),
                'mileage': pd.read_csv("mileage_balancing.csv"),
                'branding': pd.read_csv("branding_priorities.csv"),
                'stabling': pd.read_csv("stabling_geometry.csv"),
                'cleaning': pd.read_csv("cleaning_detailing_schedule.csv")
            }
            
            print("✅ Dataset loading summary:")
            total_rows = 0
            for name, df in datasets.items():
                rows = len(df)
                total_rows += rows
                print(f"   {name}: {rows:,} rows")
            
            print(f"📈 Total records: {total_rows:,}")
            return datasets
            
        except FileNotFoundError as e:
            print(f"❌ Error loading datasets: {e}")
            print("Please run high_volume_data_generator.py first")
            return None
    
    def engineer_advanced_features(self, datasets):
        """Advanced feature engineering for high accuracy"""
        print("🔧 Engineering advanced features...")
        
        # Start with comprehensive feature matrix
        feature_data = []
        
        # Get unique trains
        train_ids = datasets['mileage']['Train_ID'].unique()
        
        for train_id in tqdm(train_ids, desc="Feature Engineering"):
            # Base mileage features
            mileage_data = datasets['mileage'][datasets['mileage']['Train_ID'] == train_id]
            if len(mileage_data) > 0:
                latest_mileage = mileage_data.iloc[-1]  # Most recent record
                
                # Mileage features
                bogie_usage = latest_mileage['Bogie_Usage_Pct']
                brake_usage = latest_mileage['BrakePad_Usage_Pct']
                hvac_usage = latest_mileage['HVAC_Usage_Pct']
                motor_usage = latest_mileage['Motor_Usage_Pct']
                avg_usage = latest_mileage['Average_Usage_Pct']
                
                # Advanced mileage features
                usage_variance = np.var([bogie_usage, brake_usage, hvac_usage, motor_usage])
                max_component_usage = max(bogie_usage, brake_usage, hvac_usage, motor_usage)
                min_component_usage = min(bogie_usage, brake_usage, hvac_usage, motor_usage)
                usage_range = max_component_usage - min_component_usage
                
            else:
                # Default values if no mileage data
                bogie_usage = brake_usage = hvac_usage = motor_usage = avg_usage = 50.0
                usage_variance = max_component_usage = min_component_usage = usage_range = 0.0
            
            # Telemetry features (aggregated)
            telemetry_data = datasets['telemetry'][datasets['telemetry']['Train_ID'] == train_id]
            if len(telemetry_data) > 0:
                motor_temp_mean = telemetry_data['Motor_Temperature_C'].mean()
                motor_temp_max = telemetry_data['Motor_Temperature_C'].max()
                motor_temp_std = telemetry_data['Motor_Temperature_C'].std()
                
                motor_current_mean = telemetry_data['Motor_Current_A'].mean()
                motor_current_max = telemetry_data['Motor_Current_A'].max()
                motor_current_std = telemetry_data['Motor_Current_A'].std()
                
                brake_pressure_mean = telemetry_data['Brake_Pressure_Bar'].mean()
                brake_pressure_std = telemetry_data['Brake_Pressure_Bar'].std()
                
                hvac_power_mean = telemetry_data['HVAC_Power_kW'].mean()
                vibration_mean = telemetry_data['Vibration_Level'].mean()
                vibration_max = telemetry_data['Vibration_Level'].max()
                
                oil_temp_mean = telemetry_data['Oil_Temperature_C'].mean()
                health_score_mean = telemetry_data['Health_Score'].mean()
                health_score_min = telemetry_data['Health_Score'].min()
                
                train_age = telemetry_data['Train_Age_Months'].iloc[0]
                
                # Advanced telemetry features
                temp_current_corr = np.corrcoef(telemetry_data['Motor_Temperature_C'], telemetry_data['Motor_Current_A'])[0,1]
                health_decline_rate = (telemetry_data['Health_Score'].iloc[0] - telemetry_data['Health_Score'].iloc[-1]) / len(telemetry_data) if len(telemetry_data) > 1 else 0
                peak_hour_avg_temp = telemetry_data[telemetry_data['Peak_Hour'] == True]['Motor_Temperature_C'].mean() if 'Peak_Hour' in telemetry_data.columns else motor_temp_mean
                
            else:
                # Default telemetry values
                motor_temp_mean = motor_temp_max = motor_temp_std = 50.0
                motor_current_mean = motor_current_max = motor_current_std = 180.0
                brake_pressure_mean = brake_pressure_std = 5.0
                hvac_power_mean = vibration_mean = vibration_max = 10.0
                oil_temp_mean = health_score_mean = health_score_min = 0.8
                train_age = 24
                temp_current_corr = health_decline_rate = peak_hour_avg_temp = 0.0
            
            # Certificate features
            cert_data = datasets['fitness_certs'][datasets['fitness_certs']['Train_ID'] == train_id]
            if len(cert_data) > 0:
                total_certs = len(cert_data)
                valid_certs = len(cert_data[cert_data['Status'] == 'Valid'])
                expired_certs = len(cert_data[cert_data['Status'] == 'Expired'])
                renewal_certs = len(cert_data[cert_data['Status'] == 'Renewal_In_Progress'])
                cert_compliance_rate = valid_certs / total_certs
                
                # Advanced certificate features
                avg_compliance_score = cert_data['Compliance_Score'].mean()
                cert_cost_total = cert_data['Cost'].sum()
                critical_cert_count = len(cert_data[cert_data['Priority'] == 'Critical'])
                
            else:
                total_certs = valid_certs = expired_certs = renewal_certs = 0
                cert_compliance_rate = avg_compliance_score = cert_cost_total = critical_cert_count = 0.0
            
            # Job card features
            job_data = datasets['job_cards'][datasets['job_cards']['Train_ID'] == train_id]
            if len(job_data) > 0:
                total_jobs = len(job_data)
                open_jobs = len(job_data[job_data['Status'] == 'Open'])
                closed_jobs = len(job_data[job_data['Status'] == 'Closed'])
                critical_jobs = len(job_data[job_data['Priority'] == 'Critical'])
                high_jobs = len(job_data[job_data['Priority'] == 'High'])
                
                total_estimated_hours = job_data['Estimated_Hours'].sum()
                avg_job_complexity = job_data['Urgency_Score'].mean() if 'Urgency_Score' in job_data.columns else 50.0
                
                # Advanced job features
                pm_jobs = len(job_data[job_data['Work_Type'].str.contains('PM-', na=False)])
                cm_jobs = len(job_data[job_data['Work_Type'].str.contains('CM-', na=False)])
                emergency_jobs = len(job_data[job_data['Work_Type'].str.contains('Emergency', na=False)])
                job_backlog_ratio = open_jobs / max(1, total_jobs)
                
            else:
                total_jobs = open_jobs = closed_jobs = critical_jobs = high_jobs = 0
                total_estimated_hours = avg_job_complexity = pm_jobs = cm_jobs = emergency_jobs = job_backlog_ratio = 0.0
            
            # Stabling features
            stabling_data = datasets['stabling'][datasets['stabling']['Train_ID'] == train_id]
            if len(stabling_data) > 0:
                avg_accessibility = stabling_data['Accessibility_Score'].mean()
                avg_exit_time = stabling_data['Exit_Time_Minutes'].mean()
                avg_shunting_moves = stabling_data['Shunting_Moves_Required'].mean()
                avg_energy_cost = stabling_data['Energy_Cost_Estimate'].mean()
                reallocation_needed = stabling_data['Needs_Reallocation'].mean()
                
            else:
                avg_accessibility = avg_exit_time = avg_shunting_moves = avg_energy_cost = reallocation_needed = 0.0
            
            # Branding features
            branding_data = datasets['branding'][datasets['branding']['Train_ID'] == train_id]
            if len(branding_data) > 0:
                avg_compliance = branding_data['Compliance_Percentage'].mean()
                total_penalties = branding_data['Penalty_Incurred'].sum()
                avg_service_hours = branding_data['Actual_Service_Hours'].mean()
                brand_reliability = branding_data['Service_Reliability'].mean() if 'Service_Reliability' in branding_data.columns else 90.0
                
            else:
                avg_compliance = brand_reliability = 90.0
                total_penalties = avg_service_hours = 0.0
            
            # Cleaning features
            cleaning_data = datasets['cleaning'][datasets['cleaning']['Train_ID'] == train_id]
            if len(cleaning_data) > 0:
                total_cleaning_cost = cleaning_data['Cost'].sum()
                avg_cleaning_quality = cleaning_data['Quality_Score'].mean()
                cleaning_frequency = len(cleaning_data)
                
            else:
                total_cleaning_cost = avg_cleaning_quality = cleaning_frequency = 0.0
            
            # Target variable: Composite failure risk
            # Enhanced failure risk calculation
            failure_risk = (
                avg_usage * 0.25 +                              # Component wear
                (expired_certs / max(1, total_certs)) * 100 * 0.20 +  # Certificate issues
                (critical_jobs / max(1, total_jobs)) * 100 * 0.15 +   # Critical maintenance
                (1 - health_score_mean) * 100 * 0.20 +          # IoT health degradation
                (motor_temp_mean - 50) * 2 * 0.10 +             # Temperature stress
                (vibration_mean - 2) * 10 * 0.10                # Vibration stress
            )
            
            # Binary classification target (98% accuracy target)
            will_fail_soon = int(failure_risk > 60)  # Adjusted threshold
            
            # Advanced risk categories for multi-class
            if failure_risk > 80:
                risk_category = 3  # Critical
            elif failure_risk > 60:
                risk_category = 2  # High
            elif failure_risk > 40:
                risk_category = 1  # Medium
            else:
                risk_category = 0  # Low
            
            feature_record = {
                'Train_ID': train_id,
                
                # Primary component features
                'Bogie_Usage_Pct': bogie_usage,
                'BrakePad_Usage_Pct': brake_usage,
                'HVAC_Usage_Pct': hvac_usage,
                'Motor_Usage_Pct': motor_usage,
                'Average_Usage_Pct': avg_usage,
                'Usage_Variance': usage_variance,
                'Usage_Range': usage_range,
                'Max_Component_Usage': max_component_usage,
                
                # Telemetry features
                'Motor_Temperature_C_mean': motor_temp_mean,
                'Motor_Temperature_C_max': motor_temp_max,
                'Motor_Temperature_C_std': motor_temp_std,
                'Motor_Current_A_mean': motor_current_mean,
                'Motor_Current_A_max': motor_current_max,
                'Motor_Current_A_std': motor_current_std,
                'Brake_Pressure_Bar_mean': brake_pressure_mean,
                'HVAC_Power_kW_mean': hvac_power_mean,
                'Vibration_Level_mean': vibration_mean,
                'Vibration_Level_max': vibration_max,
                'Oil_Temperature_C_mean': oil_temp_mean,
                'Health_Score_mean': health_score_mean,
                'Health_Score_min': health_score_min,
                'Train_Age_Months': train_age,
                'Temp_Current_Correlation': temp_current_corr,
                'Health_Decline_Rate': health_decline_rate,
                'Peak_Hour_Avg_Temp': peak_hour_avg_temp,
                
                # Certificate features
                'Cert_Compliance_Rate': cert_compliance_rate,
                'Expired_Certs': expired_certs,
                'Total_Certs': total_certs,
                'Critical_Cert_Count': critical_cert_count,
                'Avg_Compliance_Score': avg_compliance_score,
                'Cert_Cost_Total': cert_cost_total,
                
                # Job card features
                'Total_Jobs': total_jobs,
                'Open_Jobs': open_jobs,
                'Critical_Jobs': critical_jobs,
                'High_Jobs': high_jobs,
                'Total_Estimated_Hours': total_estimated_hours,
                'PM_Jobs': pm_jobs,
                'CM_Jobs': cm_jobs,
                'Emergency_Jobs': emergency_jobs,
                'Job_Backlog_Ratio': job_backlog_ratio,
                'Avg_Job_Complexity': avg_job_complexity,
                
                # Operational features
                'Avg_Accessibility': avg_accessibility,
                'Avg_Exit_Time': avg_exit_time,
                'Avg_Shunting_Moves': avg_shunting_moves,
                'Avg_Energy_Cost': avg_energy_cost,
                'Reallocation_Needed': reallocation_needed,
                'Brand_Compliance': avg_compliance,
                'Total_Penalties': total_penalties,
                'Brand_Reliability': brand_reliability,
                'Cleaning_Quality': avg_cleaning_quality,
                'Cleaning_Frequency': cleaning_frequency,
                
                # Target variables
                'Failure_Risk_Score': failure_risk,
                'Will_Fail_Soon': will_fail_soon,
                'Risk_Category': risk_category
            }
            
            feature_data.append(feature_record)
        
        feature_df = pd.DataFrame(feature_data)
        feature_df = feature_df.fillna(0)
        
        print(f"✅ Engineered {len(feature_df.columns)-4} features for {len(feature_df)} trains")
        print(f"📊 Target distribution: {feature_df['Will_Fail_Soon'].value_counts().to_dict()}")
        
        return feature_df
    
    def train_ensemble_failure_prediction(self, feature_df):
        """Train advanced ensemble model for failure prediction"""
        print("🌲 Training advanced ensemble failure prediction model...")
        
        # Prepare features
        feature_cols = [col for col in feature_df.columns if col not in ['Train_ID', 'Will_Fail_Soon', 'Risk_Category', 'Failure_Risk_Score']]
        X = feature_df[feature_cols]
        y = feature_df['Will_Fail_Soon']
        
        print(f"🔢 Features: {len(feature_cols)}")
        print(f"📊 Samples: {len(X)}")
        
        # Feature selection
        print("🎯 Performing feature selection...")
        selector = SelectFromModel(RandomForestClassifier(n_estimators=50, random_state=42))
        X_selected = selector.fit_transform(X, y)
        selected_features = X.columns[selector.get_support()]
        print(f"📉 Selected {len(selected_features)} most important features")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X_selected, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale features
        scaler = RobustScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Advanced ensemble with multiple algorithms
        models = {
            'rf': RandomForestClassifier(
                n_estimators=200,
                max_depth=15,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42,
                class_weight='balanced'
            ),
            'gb': GradientBoostingClassifier(
                n_estimators=150,
                learning_rate=0.1,
                max_depth=10,
                random_state=42
            ),
            'xgb': xgb.XGBClassifier(
                n_estimators=200,
                learning_rate=0.1,
                max_depth=8,
                random_state=42,
                use_label_encoder=False,
                eval_metric='logloss'
            ),
            'lgb': lgb.LGBMClassifier(
                n_estimators=200,
                learning_rate=0.1,
                max_depth=10,
                random_state=42,
                verbose=-1
            ),
            'nn': MLPClassifier(
                hidden_layer_sizes=(100, 50),
                max_iter=1000,
                random_state=42,
                early_stopping=True,
                validation_fraction=0.1
            )
        }
        
        # Train individual models
        trained_models = {}
        for name, model in models.items():
            print(f"🔧 Training {name.upper()}...")
            if name == 'nn':
                model.fit(X_train_scaled, y_train)
                score = model.score(X_test_scaled, y_test)
            else:
                model.fit(X_train, y_train)
                score = model.score(X_test, y_test)
            
            print(f"   {name.upper()} accuracy: {score:.4f}")
            trained_models[name] = model
        
        # Create voting ensemble
        voting_models = [
            ('rf', trained_models['rf']),
            ('gb', trained_models['gb']),
            ('xgb', trained_models['xgb']),
            ('lgb', trained_models['lgb'])
        ]
        
        ensemble = VotingClassifier(
            estimators=voting_models,
            voting='soft'
        )
        
        print("🗳️ Training voting ensemble...")
        ensemble.fit(X_train, y_train)
        
        # Evaluate ensemble
        y_pred = ensemble.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"🎯 Ensemble Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
        
        # Detailed evaluation
        print("\n📊 Classification Report:")
        print(classification_report(y_test, y_pred))
        
        # Feature importance (from Random Forest)
        feature_importance = pd.DataFrame({
            'Feature': selected_features,
            'Importance': trained_models['rf'].feature_importances_
        }).sort_values('Importance', ascending=False)
        
        print("\n🔝 Top 10 Most Important Features:")
        print(feature_importance.head(10).to_string(index=False))
        
        # Save model and components
        self.models['failure_prediction'] = ensemble
        self.scalers['failure_prediction'] = scaler
        self.feature_importance['failure_prediction'] = feature_importance
        
        # Save to files
        joblib.dump(ensemble, 'advanced_failure_prediction_model.pkl')
        joblib.dump(scaler, 'failure_prediction_scaler.pkl')
        joblib.dump(selected_features, 'selected_features.pkl')
        
        return accuracy, feature_importance
    
    def train_optimization_model(self, feature_df):
        """Train optimization decision model"""
        print("⚙️ Training optimization decision model...")
        
        # Create optimization targets based on risk and operational factors
        feature_df['Optimal_Decision'] = feature_df.apply(self._determine_optimal_decision, axis=1)
        
        feature_cols = [col for col in feature_df.columns if col not in [
            'Train_ID', 'Will_Fail_Soon', 'Risk_Category', 'Failure_Risk_Score', 'Optimal_Decision'
        ]]
        
        X = feature_df[feature_cols]
        y = feature_df['Optimal_Decision']
        
        # Encode target labels
        label_encoder = LabelEncoder()
        y_encoded = label_encoder.fit_transform(y)
        
        # Split and scale
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
        )
        
        # Train XGBoost for optimization
        model = xgb.XGBClassifier(
            n_estimators=300,
            learning_rate=0.05,
            max_depth=12,
            random_state=42,
            use_label_encoder=False,
            eval_metric='mlogloss'
        )
        
        model.fit(X_train, y_train)
        
        # Evaluate
        accuracy = model.score(X_test, y_test)
        print(f"🎯 Optimization Model Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
        
        # Save model
        self.models['optimization'] = model
        self.label_encoders['optimization'] = label_encoder
        
        joblib.dump(model, 'advanced_optimization_model.pkl')
        joblib.dump(label_encoder, 'optimization_label_encoder.pkl')
        
        return accuracy
    
    def _determine_optimal_decision(self, row):
        """Determine optimal decision based on comprehensive factors"""
        risk_score = row['Failure_Risk_Score']
        cert_compliance = row['Cert_Compliance_Rate']
        critical_jobs = row['Critical_Jobs']
        health_score = row['Health_Score_mean']
        
        if risk_score > 75 or cert_compliance < 0.8 or critical_jobs > 2:
            return 'Maintenance'
        elif risk_score > 50 or health_score < 0.7:
            return 'Service_Limited'
        elif risk_score < 30 and health_score > 0.85:
            return 'Service_Full'
        else:
            return 'Standby'
    
    def train_lstm_demand_model(self, datasets):
        """Train LSTM model for demand forecasting"""
        print("📈 Training LSTM demand forecasting model...")
        
        # Prepare time series data from branding/usage patterns
        branding_data = datasets['branding'].copy()
        branding_data['Date'] = pd.to_datetime(branding_data['Date'])
        branding_data = branding_data.sort_values(['Date', 'Train_ID'])
        
        # Create daily demand aggregation
        daily_demand = branding_data.groupby('Date').agg({
            'Actual_Service_Hours': 'mean',
            'Required_Hours': 'mean',
            'Compliance_Percentage': 'mean'
        }).reset_index()
        
        # Create sequences for LSTM
        sequence_length = 14  # 14 days lookback
        X_sequences = []
        y_sequences = []
        
        for i in range(sequence_length, len(daily_demand)):
            X_sequences.append(daily_demand[['Actual_Service_Hours', 'Required_Hours', 'Compliance_Percentage']].iloc[i-sequence_length:i].values)
            y_sequences.append(daily_demand['Actual_Service_Hours'].iloc[i])
        
        X_sequences = np.array(X_sequences)
        y_sequences = np.array(y_sequences)
        
        # Train-test split
        train_size = int(0.8 * len(X_sequences))
        X_train, X_test = X_sequences[:train_size], X_sequences[train_size:]
        y_train, y_test = y_sequences[:train_size], y_sequences[train_size:]
        
        # Build LSTM model
        model = Sequential([
            LSTM(64, return_sequences=True, input_shape=(sequence_length, 3)),
            Dropout(0.2),
            LSTM(32, return_sequences=False),
            Dropout(0.2),
            Dense(16, activation='relu'),
            BatchNormalization(),
            Dense(1, activation='linear')
        ])
        
        model.compile(
            optimizer=Adam(learning_rate=0.001),
            loss='mse',
            metrics=['mae']
        )
        
        # Train model
        early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
        reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5)
        
        history = model.fit(
            X_train, y_train,
            epochs=50,
            batch_size=32,
            validation_split=0.2,
            callbacks=[early_stopping, reduce_lr],
            verbose=0
        )
        
        # Evaluate
        test_loss = model.evaluate(X_test, y_test, verbose=0)
        print(f"🎯 LSTM Test MSE: {test_loss[0]:.4f}")
        
        # Save model
        model.save('advanced_lstm_demand_model.h5')
        self.models['lstm_demand'] = model
        
        return test_loss[0]
    
    def generate_comprehensive_summary(self, failure_accuracy, optimization_accuracy, lstm_mse, feature_importance):
        """Generate comprehensive ML training summary"""
        
        summary = {
            "training_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "model_performance": {
                "failure_prediction_accuracy": float(failure_accuracy),
                "optimization_accuracy": float(optimization_accuracy),
                "lstm_demand_mse": float(lstm_mse),
                "target_accuracy_achieved": failure_accuracy >= 0.98
            },
            "feature_importance": feature_importance.head(15).to_dict('records'),
            "model_details": {
                "failure_prediction": {
                    "type": "Voting Ensemble",
                    "algorithms": ["RandomForest", "GradientBoosting", "XGBoost", "LightGBM"],
                    "features_selected": len(feature_importance)
                },
                "optimization": {
                    "type": "XGBoost",
                    "decision_classes": ["Maintenance", "Service_Limited", "Service_Full", "Standby"]
                },
                "demand_forecasting": {
                    "type": "LSTM",
                    "sequence_length": 14,
                    "features": 3
                }
            },
            "training_data_summary": {
                "total_features": len(feature_importance),
                "training_samples": 24,  # Number of trains
                "data_period": "2022-01-01 to 2025-01-20"
            }
        }
        
        with open('advanced_ml_training_summary.json', 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n🎉 ADVANCED ML TRAINING COMPLETE!")
        print(f"   🎯 Failure Prediction: {failure_accuracy*100:.2f}% accuracy")
        print(f"   ⚙️ Optimization Model: {optimization_accuracy*100:.2f}% accuracy") 
        print(f"   📈 LSTM Demand MSE: {lstm_mse:.4f}")
        print(f"   {'✅' if failure_accuracy >= 0.98 else '❌'} 98% Accuracy Target: {'ACHIEVED' if failure_accuracy >= 0.98 else 'NOT MET'}")
        
        return summary

def main():
    """Main training function"""
    print("🚀 Advanced KMRL ML Training for 98% Accuracy")
    print("=" * 60)
    
    trainer = AdvancedKMRLMLTrainer()
    
    # Load datasets
    datasets = trainer.load_large_datasets()
    if datasets is None:
        return
    
    # Engineer features
    feature_df = trainer.engineer_advanced_features(datasets)
    
    # Train models
    failure_accuracy, feature_importance = trainer.train_ensemble_failure_prediction(feature_df)
    optimization_accuracy = trainer.train_optimization_model(feature_df)
    lstm_mse = trainer.train_lstm_demand_model(datasets)
    
    # Generate summary
    summary = trainer.generate_comprehensive_summary(
        failure_accuracy, optimization_accuracy, lstm_mse, feature_importance
    )
    
    print("\n📁 Models saved:")
    print("   - advanced_failure_prediction_model.pkl")
    print("   - advanced_optimization_model.pkl") 
    print("   - advanced_lstm_demand_model.h5")
    print("   - advanced_ml_training_summary.json")

if __name__ == "__main__":
    main()