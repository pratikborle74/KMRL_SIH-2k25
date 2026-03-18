#!/usr/bin/env python
"""
FORCE ALL TEXT TO BE BLACK - AGGRESSIVE APPROACH
This script ensures ALL text elements are forced to black color
"""

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import warnings
warnings.filterwarnings('ignore')

def force_all_text_black():
    """
    AGGRESSIVE function to force ALL text to be BLACK
    This overrides any default matplotlib settings
    """
    # Reset to default first
    mpl.rcdefaults()
    
    # Set ALL possible text properties to BLACK
    plt.rcParams.update({
        # ALL TEXT COLORS - FORCE BLACK
        'text.color': '#000000',           # Pure black
        'axes.labelcolor': '#000000',      # Axis labels black
        'axes.titlecolor': '#000000',      # Title black  
        'xtick.color': '#000000',          # X tick marks black
        'ytick.color': '#000000',          # Y tick marks black
        'xtick.labelsize': 11,
        'ytick.labelsize': 11,
        'legend.edgecolor': '#000000',     # Legend border black
        'legend.facecolor': 'white',       # Legend background white
        
        # BACKGROUNDS - WHITE
        'figure.facecolor': 'white',       # Figure background white
        'axes.facecolor': 'white',         # Plot area white
        'savefig.facecolor': 'white',      # Save background white
        
        # AXES AND SPINES - BLACK
        'axes.edgecolor': '#000000',       # Axes border black
        'axes.linewidth': 1.5,             # Thicker axes
        
        # FONT PROPERTIES - BLACK AND BOLD
        'font.size': 12,
        'font.weight': 'bold',
        'axes.titlesize': 16,
        'axes.titleweight': 'bold',
        'axes.labelsize': 14,
        'axes.labelweight': 'bold',
        'legend.fontsize': 12,
        
        # GRID - LIGHT GRAY
        'grid.color': '#CCCCCC',
        'grid.alpha': 0.5,
        'grid.linewidth': 0.5,
    })
    
    # Additional matplotlib settings
    mpl.rcParams['text.color'] = '#000000'

def create_test_graph_with_black_text():
    """Create a test graph with ALL BLACK TEXT"""
    
    # Force all text to be black
    force_all_text_black()
    
    print("🎨 Creating test graph with FORCED BLACK TEXT...")
    
    # Create sample data
    x = np.linspace(0, 10, 50)
    y1 = np.sin(x) + 0.2 * np.random.randn(50)
    y2 = np.cos(x) + 0.2 * np.random.randn(50)
    
    # Create figure with subplots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('TEST: ALL TEXT SHOULD BE BLACK', fontsize=18, fontweight='bold', color='#000000')
    
    # Plot 1: Line plot
    ax1.plot(x, y1, 'b-', linewidth=2, label='Data 1', color='blue')
    ax1.plot(x, y2, 'r--', linewidth=2, label='Data 2', color='red')
    ax1.set_title('Line Plot - TEXT SHOULD BE BLACK', fontsize=14, fontweight='bold', color='#000000')
    ax1.set_xlabel('X Axis Label', fontsize=12, fontweight='bold', color='#000000')
    ax1.set_ylabel('Y Axis Label', fontsize=12, fontweight='bold', color='#000000')
    ax1.legend(loc='upper right')
    ax1.grid(True, alpha=0.3)
    ax1.tick_params(colors='#000000', labelsize=10)
    
    # Manually set tick label colors
    for label in ax1.get_xticklabels():
        label.set_color('#000000')
        label.set_fontweight('bold')
    for label in ax1.get_yticklabels():
        label.set_color('#000000')
        label.set_fontweight('bold')
    
    # Plot 2: Bar chart
    categories = ['A', 'B', 'C', 'D', 'E']
    values = [23, 45, 56, 78, 32]
    bars = ax2.bar(categories, values, color=['red', 'blue', 'green', 'orange', 'purple'], alpha=0.7)
    ax2.set_title('Bar Chart - TEXT SHOULD BE BLACK', fontsize=14, fontweight='bold', color='#000000')
    ax2.set_xlabel('Categories', fontsize=12, fontweight='bold', color='#000000')
    ax2.set_ylabel('Values', fontsize=12, fontweight='bold', color='#000000')
    ax2.tick_params(colors='#000000', labelsize=10)
    ax2.grid(True, alpha=0.3)
    
    # Add value labels on bars
    for bar, val in zip(bars, values):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{val}', ha='center', va='bottom', 
                fontweight='bold', color='#000000', fontsize=10)
    
    # Manually set tick label colors for plot 2
    for label in ax2.get_xticklabels():
        label.set_color('#000000')
        label.set_fontweight('bold')
    for label in ax2.get_yticklabels():
        label.set_color('#000000')
        label.set_fontweight('bold')
    
    # Plot 3: Scatter plot
    np.random.seed(42)
    x_scatter = np.random.randn(30)
    y_scatter = np.random.randn(30)
    colors = np.random.rand(30)
    ax3.scatter(x_scatter, y_scatter, c=colors, cmap='viridis', alpha=0.7, s=50)
    ax3.set_title('Scatter Plot - TEXT SHOULD BE BLACK', fontsize=14, fontweight='bold', color='#000000')
    ax3.set_xlabel('X Data', fontsize=12, fontweight='bold', color='#000000')
    ax3.set_ylabel('Y Data', fontsize=12, fontweight='bold', color='#000000')
    ax3.tick_params(colors='#000000', labelsize=10)
    ax3.grid(True, alpha=0.3)
    
    # Manually set tick label colors for plot 3
    for label in ax3.get_xticklabels():
        label.set_color('#000000')
        label.set_fontweight('bold')
    for label in ax3.get_yticklabels():
        label.set_color('#000000')
        label.set_fontweight('bold')
    
    # Plot 4: Histogram
    data = np.random.normal(0, 1, 1000)
    ax4.hist(data, bins=25, color='skyblue', alpha=0.7, edgecolor='#000000')
    ax4.set_title('Histogram - TEXT SHOULD BE BLACK', fontsize=14, fontweight='bold', color='#000000')
    ax4.set_xlabel('Values', fontsize=12, fontweight='bold', color='#000000')
    ax4.set_ylabel('Frequency', fontsize=12, fontweight='bold', color='#000000')
    ax4.tick_params(colors='#000000', labelsize=10)
    ax4.grid(True, alpha=0.3)
    
    # Manually set tick label colors for plot 4
    for label in ax4.get_xticklabels():
        label.set_color('#000000')
        label.set_fontweight('bold')
    for label in ax4.get_yticklabels():
        label.set_color('#000000')
        label.set_fontweight('bold')
    
    # Adjust layout
    plt.tight_layout()
    
    # Save with specific settings
    plt.savefig('forced_black_text_test.png', 
                dpi=300, 
                facecolor='white', 
                edgecolor='none',
                bbox_inches='tight')
    
    plt.show()
    
    print("✅ Test graph saved: forced_black_text_test.png")
    print("🔍 CHECK: ALL text should now be BLACK/DARK!")

def create_simple_kmrl_chart():
    """Create simple KMRL chart with forced black text"""
    
    force_all_text_black()
    
    print("📊 Creating KMRL chart with FORCED BLACK TEXT...")
    
    # KMRL data
    models = ['Failure\nPrediction', 'Optimization\nDecision', 'Demand\nForecasting']
    accuracies = [98.6, 100.0, 50.0]
    colors = ['#2E8B57', '#4169E1', '#FF6347']
    
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    fig.suptitle('KMRL ML Models - FORCED BLACK TEXT', 
                 fontsize=18, fontweight='bold', color='#000000')
    
    # Create bars
    bars = ax.bar(models, accuracies, color=colors, alpha=0.8, edgecolor='#000000', linewidth=2)
    
    # Set title and labels with explicit black color
    ax.set_title('Model Accuracy Results', fontsize=14, fontweight='bold', color='#000000')
    ax.set_ylabel('Accuracy (%)', fontsize=12, fontweight='bold', color='#000000')
    ax.set_xlabel('ML Models', fontsize=12, fontweight='bold', color='#000000')
    ax.set_ylim(0, 105)
    ax.grid(True, alpha=0.3)
    ax.tick_params(colors='#000000', labelsize=11)
    
    # Add percentage labels on bars
    for bar, acc in zip(bars, accuracies):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 2,
                f'{acc:.1f}%', ha='center', va='bottom', 
                fontweight='bold', fontsize=12, color='#000000')
    
    # Force tick labels to be black
    for label in ax.get_xticklabels():
        label.set_color('#000000')
        label.set_fontweight('bold')
    for label in ax.get_yticklabels():
        label.set_color('#000000')
        label.set_fontweight('bold')
    
    plt.tight_layout()
    plt.savefig('kmrl_forced_black_text.png', 
                dpi=300, 
                facecolor='white', 
                edgecolor='none',
                bbox_inches='tight')
    
    plt.show()
    
    print("✅ KMRL chart saved: kmrl_forced_black_text.png")
    print("🔍 CHECK: ALL text should be BLACK!")

def main():
    """Main function"""
    
    print("🚨 FORCING ALL TEXT TO BE BLACK - AGGRESSIVE METHOD")
    print("=" * 55)
    
    # Create test graphs
    create_test_graph_with_black_text()
    print()
    create_simple_kmrl_chart()
    
    print("\n" + "=" * 55)
    print("✅ GRAPHS CREATED WITH FORCED BLACK TEXT!")
    print("📁 Files created:")
    print("   • forced_black_text_test.png")
    print("   • kmrl_forced_black_text.png")
    print("🔍 If text is still light, the issue may be:")
    print("   1. Display/monitor settings")
    print("   2. Image viewer settings") 
    print("   3. System theme overrides")
    print("=" * 55)

if __name__ == "__main__":
    main()