#!/usr/bin/env python
"""
Enhanced LSTM Demand Forecasting Model - Improved Training & Metrics
Advanced metrics: MAE, MAPE, R², accuracy within tolerance, detailed training progress
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import warnings
warnings.filterwarnings('ignore')

# TensorFlow/Keras with proper error handling
try:
    import tensorflow as tf
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import LSTM, Dense, Dropout
    from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
    tf_available = True
    print("✅ TensorFlow/Keras available")
except ImportError:
    tf_available = False
    print("⚠️ TensorFlow/Keras not available - using simple forecasting")

def create_sequences(data, seq_length=30):
    """Create sequences for LSTM training"""
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:(i + seq_length)])
        y.append(data[i + seq_length])
    return np.array(X), np.array(y)

def calculate_accuracy_within_tolerance(y_true, y_pred, tolerance=0.1):
    """Calculate accuracy within tolerance (±10%)"""
    relative_error = np.abs((y_true - y_pred) / (y_true + 1e-8))
    within_tolerance = np.mean(relative_error <= tolerance)
    return within_tolerance

def enhanced_lstm_demand_forecasting():
    """Enhanced LSTM demand forecasting with comprehensive metrics"""
    
    print("🚀 ENHANCED LSTM DEMAND FORECASTING MODEL")
    print("=" * 60)
    
    try:
        # Load demand data
        job_cards = pd.read_csv("maximo_job_cards.csv")
        
        # Create comprehensive demand features
        print("⚙️ Preparing demand data...")
        
        # Convert date and extract time features
        job_cards['Created_Date'] = pd.to_datetime(job_cards['Created_Date'])
        job_cards['Year'] = job_cards['Created_Date'].dt.year
        job_cards['Month'] = job_cards['Created_Date'].dt.month
        job_cards['Day'] = job_cards['Created_Date'].dt.day
        job_cards['DayOfWeek'] = job_cards['Created_Date'].dt.dayofweek
        job_cards['Quarter'] = job_cards['Created_Date'].dt.quarter
        
        # Create demand features
        daily_demand = job_cards.groupby('Created_Date').agg({
            'Work_Order_ID': 'count',
            'Priority': lambda x: (x == 'Critical').sum(),
            'Estimated_Hours': ['sum', 'mean'],
            'Train_ID': 'nunique'
        }).reset_index()
        
        daily_demand.columns = ['Date', 'Total_Jobs', 'Critical_Jobs', 'Total_Hours', 'Avg_Hours', 'Trains_Affected']
        
        # Add time-based features for better LSTM performance
        daily_demand['Year'] = daily_demand['Date'].dt.year
        daily_demand['Month'] = daily_demand['Date'].dt.month
        daily_demand['Day'] = daily_demand['Date'].dt.day
        daily_demand['DayOfWeek'] = daily_demand['Date'].dt.dayofweek
        daily_demand['Quarter'] = daily_demand['Date'].dt.quarter
        
        # Create trend and seasonal features
        daily_demand = daily_demand.sort_values('Date').reset_index(drop=True)
        daily_demand['Trend'] = range(len(daily_demand))
        daily_demand['Season_Sin'] = np.sin(2 * np.pi * daily_demand['Month'] / 12)
        daily_demand['Season_Cos'] = np.cos(2 * np.pi * daily_demand['Month'] / 12)
        
        print(f"📊 Prepared {len(daily_demand)} days of demand data")
        
        if tf_available:
            # Enhanced LSTM approach
            print("🧠 Training Enhanced LSTM Model...")
            
            # Prepare features for LSTM
            feature_cols = ['Total_Jobs', 'Critical_Jobs', 'Total_Hours', 'Avg_Hours', 
                          'Trains_Affected', 'Month', 'DayOfWeek', 'Quarter', 
                          'Trend', 'Season_Sin', 'Season_Cos']
            
            features = daily_demand[feature_cols].values
            target = daily_demand['Total_Jobs'].values
            
            # Scale features
            feature_scaler = MinMaxScaler()
            target_scaler = MinMaxScaler()
            
            features_scaled = feature_scaler.fit_transform(features)
            target_scaled = target_scaler.fit_transform(target.reshape(-1, 1)).flatten()
            
            # Create sequences
            seq_length = min(5, len(features_scaled) // 4)  # Smaller sequence for small dataset
            if seq_length < 3:
                seq_length = 3
            
            X, y = create_sequences(features_scaled, seq_length)
            
            print(f"📊 Created {len(X)} sequences with length {seq_length}")
            
            # Split data ensuring minimum test size
            if len(X) < 10:
                # Very small dataset - use simple split
                split_idx = max(1, len(X) - 3)
            else:
                split_idx = int(0.8 * len(X))
            
            X_train, X_test = X[:split_idx], X[split_idx:]
            y_train, y_test = y[:split_idx], y[split_idx:]
            
            print(f"📊 Train: {len(X_train)} samples, Test: {len(X_test)} samples")
            
            # Enhanced LSTM model architecture
            model = Sequential([
                LSTM(128, return_sequences=True, input_shape=(seq_length, features_scaled.shape[1])),
                Dropout(0.3),
                LSTM(64, return_sequences=True),
                Dropout(0.3),
                LSTM(32, return_sequences=False),
                Dropout(0.2),
                Dense(16, activation='relu'),
                Dense(1, activation='linear')
            ])
            
            # Compile with advanced optimizer
            model.compile(
                optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
                loss='mse',
                metrics=['mae']
            )
            
            print("🏗️ LSTM Architecture:")
            print(f"   • Input: ({seq_length}, {features_scaled.shape[1]})")
            print("   • LSTM Layers: 128→64→32 units")
            print("   • Dropout: 0.3, 0.3, 0.2")
            print("   • Dense: 16→1 units")
            
            # Enhanced callbacks
            callbacks = [
                EarlyStopping(monitor='val_loss', patience=20, restore_best_weights=True),
                ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=10, min_lr=1e-6)
            ]
            
            # Train model with validation
            print("🔥 Training Enhanced LSTM...")
            history = model.fit(
                X_train, y_train,
                epochs=100,
                batch_size=16,
                validation_data=(X_test, y_test),
                callbacks=callbacks,
                verbose=1
            )
            
            # Predictions
            y_pred_scaled = model.predict(X_test)
            y_pred = target_scaler.inverse_transform(y_pred_scaled).flatten()
            y_test_original = target_scaler.inverse_transform(y_test.reshape(-1, 1)).flatten()
            
            # Ensure same length for metrics calculation
            min_len = min(len(y_pred), len(y_test_original))
            y_pred = y_pred[:min_len]
            y_test_original = y_test_original[:min_len]
            
            # Comprehensive metrics
            mse = mean_squared_error(y_test_original, y_pred)
            mae = mean_absolute_error(y_test_original, y_pred)
            rmse = np.sqrt(mse)
            r2 = r2_score(y_test_original, y_pred)
            mape = np.mean(np.abs((y_test_original - y_pred) / (y_test_original + 1e-8))) * 100
            accuracy_10 = calculate_accuracy_within_tolerance(y_test_original, y_pred, 0.1)
            accuracy_20 = calculate_accuracy_within_tolerance(y_test_original, y_pred, 0.2)
            
            print("\\n🎯 ENHANCED LSTM PERFORMANCE METRICS:")
            print("="*50)
            print(f"📊 Root Mean Square Error: {rmse:.3f}")
            print(f"📊 Mean Absolute Error: {mae:.3f}")
            print(f"📊 Mean Absolute % Error: {mape:.2f}%")
            print(f"📊 R² Score: {r2:.3f}")
            print(f"📊 Accuracy (±10%): {accuracy_10:.1%}")
            print(f"📊 Accuracy (±20%): {accuracy_20:.1%}")
            print("="*50)
            
            # Training progress metrics
            final_train_loss = history.history['loss'][-1]
            final_val_loss = history.history['val_loss'][-1]
            final_train_mae = history.history['mae'][-1]
            final_val_mae = history.history['val_mae'][-1]
            
            print("\\n📈 TRAINING PROGRESS:")
            print("="*30)
            print(f"🏋️ Final Training Loss: {final_train_loss:.4f}")
            print(f"🔍 Final Validation Loss: {final_val_loss:.4f}")
            print(f"🏋️ Final Training MAE: {final_train_mae:.4f}")
            print(f"🔍 Final Validation MAE: {final_val_mae:.4f}")
            print(f"📊 Epochs Completed: {len(history.history['loss'])}")
            print("="*30)
            
            # Overfitting check
            if final_val_loss > final_train_loss * 1.5:
                print("⚠️ Warning: Potential overfitting detected")
            else:
                print("✅ Model shows good generalization")
            
            # Save enhanced model
            model.save('enhanced_lstm_model.h5')
            
            # Create prediction visualization with DARK BLACK text
            plt.style.use('default')  # Ensure default style
            plt.rcParams.update({
                # ALL TEXT COLORS TO BLACK
                'text.color': 'black',
                'axes.labelcolor': 'black',
                'xtick.color': 'black',
                'ytick.color': 'black',
                'axes.titlecolor': 'black',
                'axes.edgecolor': 'black',
                'legend.edgecolor': 'black',
                
                # BACKGROUND COLORS
                'figure.facecolor': 'white',
                'axes.facecolor': 'white',
                'savefig.facecolor': 'white',
                
                # FONT SETTINGS FOR DARK TEXT
                'font.size': 11,
                'axes.titlesize': 14,
                'axes.labelsize': 12,
                'xtick.labelsize': 10,
                'ytick.labelsize': 10,
                'legend.fontsize': 10,
                'font.weight': 'bold'
            })
            
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
            fig.patch.set_facecolor('white')
            
            # Plot 1: Loss Progress
            ax1.plot(history.history['loss'], label='Training Loss', color='blue')
            ax1.plot(history.history['val_loss'], label='Validation Loss', color='red')
            ax1.set_title('Model Loss Progress', color='black', fontsize=12, fontweight='bold')
            ax1.set_xlabel('Epoch', color='black', fontsize=10)
            ax1.set_ylabel('Loss', color='black', fontsize=10)
            ax1.legend()
            ax1.grid(True, alpha=0.3)
            ax1.tick_params(colors='black')
            
            # Plot 2: MAE Progress
            ax2.plot(history.history['mae'], label='Training MAE', color='green')
            ax2.plot(history.history['val_mae'], label='Validation MAE', color='orange')
            ax2.set_title('Model MAE Progress', color='black', fontsize=12, fontweight='bold')
            ax2.set_xlabel('Epoch', color='black', fontsize=10)
            ax2.set_ylabel('MAE', color='black', fontsize=10)
            ax2.legend()
            ax2.grid(True, alpha=0.3)
            ax2.tick_params(colors='black')
            
            # Plot 3: Predictions vs Actual
            ax3.scatter(y_test_original, y_pred, alpha=0.7, color='purple')
            ax3.plot([y_test_original.min(), y_test_original.max()], 
                    [y_test_original.min(), y_test_original.max()], 'r--', lw=2)
            ax3.set_xlabel('Actual Demand', color='black', fontsize=10)
            ax3.set_ylabel('Predicted Demand', color='black', fontsize=10)
            ax3.set_title(f'Predictions vs Actual (R²={r2:.3f})', color='black', fontsize=12, fontweight='bold')
            ax3.grid(True, alpha=0.3)
            ax3.tick_params(colors='black')
            
            # Plot 4: Residual Distribution
            residuals = y_test_original - y_pred
            ax4.hist(residuals, bins=10, alpha=0.7, edgecolor='black', facecolor='lightblue')
            ax4.set_xlabel('Residuals', color='black', fontsize=10)
            ax4.set_ylabel('Frequency', color='black', fontsize=10)
            ax4.set_title('Residual Distribution', color='black', fontsize=12, fontweight='bold')
            ax4.grid(True, alpha=0.3)
            ax4.tick_params(colors='black')
            
            plt.tight_layout()
            plt.savefig('enhanced_lstm_results.png', dpi=300, bbox_inches='tight')
            print("\\n💾 Saved Enhanced LSTM Results:")
            print("   • enhanced_lstm_model.h5")
            print("   • enhanced_lstm_results.png")
            
            return {
                'rmse': rmse, 'mae': mae, 'r2': r2, 'mape': mape,
                'accuracy_10': accuracy_10, 'accuracy_20': accuracy_20,
                'training_epochs': len(history.history['loss'])
            }
            
        else:
            # Simple forecasting fallback
            print("📊 Using Simple Moving Average Forecasting...")
            
            target = daily_demand['Total_Jobs'].values
            window = min(7, len(target) // 3)
            
            predictions = []
            actuals = []
            
            for i in range(window, len(target)):
                pred = np.mean(target[i-window:i])
                predictions.append(pred)
                actuals.append(target[i])
            
            predictions = np.array(predictions)
            actuals = np.array(actuals)
            
            # Simple metrics
            mae = mean_absolute_error(actuals, predictions)
            rmse = np.sqrt(mean_squared_error(actuals, predictions))
            r2 = r2_score(actuals, predictions)
            
            print("\\n📊 SIMPLE FORECASTING METRICS:")
            print(f"   • RMSE: {rmse:.3f}")
            print(f"   • MAE: {mae:.3f}")
            print(f"   • R²: {r2:.3f}")
            
            return {'rmse': rmse, 'mae': mae, 'r2': r2}
            
    except Exception as e:
        print(f"❌ Error in LSTM forecasting: {e}")
        return {'error': str(e)}

if __name__ == "__main__":
    results = enhanced_lstm_demand_forecasting()
    
    print(f"\\n" + "="*60)
    print(f"🏆 ENHANCED LSTM DEMAND FORECASTING RESULTS")
    print(f"="*60)
    
    if 'error' not in results:
        if 'mape' in results:  # Full LSTM results
            print(f"📊 RMSE: {results['rmse']:.3f}")
            print(f"📊 MAE: {results['mae']:.3f}")
            print(f"📊 MAPE: {results['mape']:.2f}%")
            print(f"📊 R²: {results['r2']:.3f}")
            print(f"📊 Accuracy (±10%): {results['accuracy_10']:.1%}")
            print(f"📊 Training Epochs: {results['training_epochs']}")
            print("\\n✅ Enhanced LSTM model trained successfully!")
            print("🚀 Ready for KMRL demand forecasting!")
        else:  # Simple forecasting results
            print(f"📊 RMSE: {results['rmse']:.3f}")
            print(f"📊 MAE: {results['mae']:.3f}")
            print(f"📊 R²: {results['r2']:.3f}")
            print("\\n✅ Simple forecasting completed!")
    else:
        print(f"❌ Error: {results['error']}")