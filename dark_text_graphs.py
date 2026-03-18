#!/usr/bin/env python
"""
Simple Dark Text Graphs - Ensures ALL TEXT is BLACK/DARK
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

def make_all_text_dark():
    """Force ALL text to be dark/black"""
    plt.rcParams.update({
        # ALL TEXT COLORS TO BLACK
        'text.color': 'black',
        'axes.labelcolor': 'black', 
        'axes.titlecolor': 'black',
        'xtick.color': 'black',
        'ytick.color': 'black',
        'legend.edgecolor': 'black',
        'legend.facecolor': 'white',
        
        # BACKGROUND COLORS
        'figure.facecolor': 'white',
        'axes.facecolor': 'white',
        'savefig.facecolor': 'white',
        
        # FONT SETTINGS
        'font.size': 11,
        'axes.titlesize': 14,
        'axes.labelsize': 12,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 10,
        'font.weight': 'bold'
    })

def create_dark_text_sample_graphs():
    """Create sample graphs with dark text"""
    
    make_all_text_dark()
    
    print("📊 Creating Sample Graphs with DARK TEXT...")
    
    # Sample data
    x = np.linspace(0, 10, 100)
    y1 = np.sin(x)
    y2 = np.cos(x)
    
    # Create figure with 4 subplots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('KMRL Sample Graphs - ALL TEXT IS DARK BLACK', 
                 fontsize=16, fontweight='bold', color='black')
    
    # Plot 1: Line plot
    ax1.plot(x, y1, 'b-', linewidth=2, label='Sin(x)')
    ax1.plot(x, y2, 'r--', linewidth=2, label='Cos(x)')
    ax1.set_title('Line Plot Example', color='black', fontweight='bold')
    ax1.set_xlabel('X Values', color='black', fontweight='bold')
    ax1.set_ylabel('Y Values', color='black', fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.tick_params(colors='black')
    
    # Plot 2: Bar chart
    categories = ['Model A', 'Model B', 'Model C', 'Model D']
    values = [85, 92, 78, 95]
    bars = ax2.bar(categories, values, color=['blue', 'red', 'green', 'orange'], alpha=0.7)
    ax2.set_title('Model Performance', color='black', fontweight='bold')
    ax2.set_xlabel('Models', color='black', fontweight='bold')  
    ax2.set_ylabel('Accuracy (%)', color='black', fontweight='bold')
    ax2.tick_params(colors='black')
    ax2.grid(True, alpha=0.3)
    
    # Add value labels on bars
    for bar, val in zip(bars, values):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{val}%', ha='center', va='bottom', 
                fontweight='bold', color='black')
    
    # Plot 3: Scatter plot
    np.random.seed(42)
    x_scatter = np.random.randn(50)
    y_scatter = np.random.randn(50)
    ax3.scatter(x_scatter, y_scatter, c='purple', alpha=0.6, s=60)
    ax3.set_title('Scatter Plot Example', color='black', fontweight='bold')
    ax3.set_xlabel('X Data', color='black', fontweight='bold')
    ax3.set_ylabel('Y Data', color='black', fontweight='bold')
    ax3.tick_params(colors='black')
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Histogram
    data = np.random.normal(0, 1, 1000)
    ax4.hist(data, bins=30, color='lightblue', edgecolor='black', alpha=0.7)
    ax4.set_title('Histogram Example', color='black', fontweight='bold')
    ax4.set_xlabel('Values', color='black', fontweight='bold')
    ax4.set_ylabel('Frequency', color='black', fontweight='bold')
    ax4.tick_params(colors='black')
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('dark_text_sample_graphs.png', dpi=300, facecolor='white', 
                bbox_inches='tight')
    plt.show()
    
    print("✅ Sample graphs saved: dark_text_sample_graphs.png")
    print("✅ ALL TEXT IS DARK BLACK!")

def create_kmrl_performance_chart():
    """Create KMRL performance chart with dark text"""
    
    make_all_text_dark()
    
    print("📈 Creating KMRL Performance Chart with DARK TEXT...")
    
    # KMRL model performance data
    models = ['Failure\nPrediction', 'Optimization\nDecision', 'Demand\nForecasting']
    accuracies = [98.6, 100.0, 50.0]
    colors = ['#2E8B57', '#4169E1', '#FF6347']
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('KMRL ML System Performance - DARK TEXT', 
                 fontsize=18, fontweight='bold', color='black')
    
    # Bar chart
    bars = ax1.bar(models, accuracies, color=colors, alpha=0.8, edgecolor='black', linewidth=2)
    ax1.set_title('Model Accuracy Comparison', fontweight='bold', color='black')
    ax1.set_ylabel('Accuracy (%)', color='black', fontweight='bold')
    ax1.set_ylim(0, 105)
    ax1.grid(True, alpha=0.3)
    ax1.tick_params(colors='black')
    
    # Add percentage labels on bars
    for bar, acc in zip(bars, accuracies):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 2,
                f'{acc:.1f}%', ha='center', va='bottom', 
                fontweight='bold', fontsize=12, color='black')
    
    # Pie chart
    readiness = [82.9, 17.1]
    labels = ['Production\nReady', 'Needs\nImprovement']
    colors_pie = ['#32CD32', '#FFA500']
    
    wedges, texts, autotexts = ax2.pie(readiness, labels=labels, colors=colors_pie, 
                                      autopct='%1.1f%%', startangle=90)
    ax2.set_title('System Deployment Readiness', fontweight='bold', color='black')
    
    # Make pie chart text black
    for text in texts:
        text.set_color('black')
        text.set_fontweight('bold')
    
    for autotext in autotexts:
        autotext.set_color('black')
        autotext.set_fontweight('bold')
    
    plt.tight_layout()
    plt.savefig('kmrl_performance_dark_text.png', dpi=300, facecolor='white', 
                bbox_inches='tight')
    plt.show()
    
    print("✅ KMRL chart saved: kmrl_performance_dark_text.png")
    print("✅ ALL TEXT IS DARK BLACK!")

def create_simple_lstm_chart():
    """Create simple LSTM training chart with dark text"""
    
    make_all_text_dark()
    
    print("🧠 Creating LSTM Training Chart with DARK TEXT...")
    
    # Sample training data
    epochs = range(1, 51)
    train_loss = 0.5 * np.exp(-np.array(epochs) * 0.1) + np.random.normal(0, 0.02, len(epochs))
    val_loss = 0.6 * np.exp(-np.array(epochs) * 0.08) + np.random.normal(0, 0.03, len(epochs))
    
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    fig.suptitle('LSTM Training Progress - DARK TEXT', 
                 fontsize=16, fontweight='bold', color='black')
    
    ax.plot(epochs, train_loss, 'b-', linewidth=3, label='Training Loss')
    ax.plot(epochs, val_loss, 'r--', linewidth=3, label='Validation Loss')
    ax.set_title('Model Loss Over Epochs', fontweight='bold', color='black')
    ax.set_xlabel('Epoch', color='black', fontweight='bold')
    ax.set_ylabel('Loss', color='black', fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.tick_params(colors='black')
    
    plt.tight_layout()
    plt.savefig('lstm_training_dark_text.png', dpi=300, facecolor='white', 
                bbox_inches='tight')
    plt.show()
    
    print("✅ LSTM chart saved: lstm_training_dark_text.png")
    print("✅ ALL TEXT IS DARK BLACK!")

def main():
    """Main function to create all dark text graphs"""
    
    print("🎨 CREATING GRAPHS WITH DARK BLACK TEXT")
    print("=" * 50)
    
    # Create all graphs with dark text
    create_dark_text_sample_graphs()
    print()
    create_kmrl_performance_chart()
    print()
    create_simple_lstm_chart()
    
    print("\n" + "=" * 50)
    print("✅ ALL GRAPHS CREATED WITH DARK BLACK TEXT!")
    print("📁 Files created:")
    print("   • dark_text_sample_graphs.png")
    print("   • kmrl_performance_dark_text.png") 
    print("   • lstm_training_dark_text.png")
    print("🎯 ALL TEXT IS NOW DARK/BLACK COLORED!")
    print("=" * 50)

if __name__ == "__main__":
    main()