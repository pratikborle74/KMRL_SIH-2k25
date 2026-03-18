#!/usr/bin/env python
"""
ULTRA AGGRESSIVE BLACK TEXT - MANUAL COLOR SETTING
This manually sets EVERY text element to pure black #000000
"""

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import warnings
warnings.filterwarnings('ignore')

def ultra_force_black_text():
    """ULTRA aggressive function to force ALL text to PURE BLACK"""
    
    # Complete reset
    plt.clf()
    plt.cla()
    mpl.rcdefaults()
    
    # Set EVERY possible parameter to force black text
    params = {
        # TEXT COLORS - ALL BLACK
        'text.color': '#000000',
        'axes.labelcolor': '#000000',
        'axes.titlecolor': '#000000',
        'xtick.color': '#000000',
        'ytick.color': '#000000',
        'xtick.labelcolor': '#000000',
        'ytick.labelcolor': '#000000',
        'legend.edgecolor': '#000000',
        'legend.labelcolor': '#000000',
        
        # BACKGROUNDS - WHITE
        'figure.facecolor': 'white',
        'axes.facecolor': 'white',
        'savefig.facecolor': 'white',
        'legend.facecolor': 'white',
        
        # AXES - BLACK
        'axes.edgecolor': '#000000',
        'axes.linewidth': 2,
        'axes.spines.left': True,
        'axes.spines.bottom': True,
        'axes.spines.top': True,
        'axes.spines.right': True,
        
        # FONTS - BLACK AND LARGE
        'font.size': 14,
        'font.weight': 'bold',
        'axes.titlesize': 18,
        'axes.titleweight': 'bold',
        'axes.labelsize': 16,
        'axes.labelweight': 'bold',
        'xtick.labelsize': 12,
        'ytick.labelsize': 12,
        'legend.fontsize': 12,
        
        # TICKS - BLACK
        'xtick.major.size': 8,
        'ytick.major.size': 8,
        'xtick.minor.size': 4,
        'ytick.minor.size': 4,
        'xtick.major.width': 2,
        'ytick.major.width': 2,
        'xtick.direction': 'inout',
        'ytick.direction': 'inout',
        
        # GRID - LIGHT
        'grid.color': '#DDDDDD',
        'grid.alpha': 0.7,
        'grid.linewidth': 1,
    }
    
    plt.rcParams.update(params)
    mpl.rcParams.update(params)

def create_ultra_black_test():
    """Create test with ULTRA BLACK text"""
    
    ultra_force_black_text()
    
    print("🚨 Creating ULTRA BLACK TEXT test...")
    
    # Simple test chart
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    
    # Data
    categories = ['Test A', 'Test B', 'Test C', 'Test D']
    values = [25, 50, 75, 100]
    colors = ['red', 'blue', 'green', 'orange']
    
    # Create bars
    bars = ax.bar(categories, values, color=colors, alpha=0.7, edgecolor='#000000', linewidth=3)
    
    # Set ALL text elements manually to pure black
    fig.suptitle('ULTRA BLACK TEXT TEST - ALL TEXT PURE BLACK #000000', 
                 fontsize=20, fontweight='bold', color='#000000')
    
    ax.set_title('THIS SHOULD BE PURE BLACK TEXT', 
                 fontsize=16, fontweight='bold', color='#000000')
    ax.set_xlabel('CATEGORIES - BLACK TEXT', 
                  fontsize=14, fontweight='bold', color='#000000')
    ax.set_ylabel('VALUES - BLACK TEXT', 
                  fontsize=14, fontweight='bold', color='#000000')
    
    # Force tick parameters
    ax.tick_params(axis='both', colors='#000000', labelsize=12, width=2, length=6)
    ax.grid(True, alpha=0.3)
    
    # Add value labels with pure black
    for bar, val in zip(bars, values):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 2,
                f'{val}%', ha='center', va='bottom', 
                fontsize=14, fontweight='bold', color='#000000')
    
    # MANUALLY force every tick label to pure black
    plt.setp(ax.get_xticklabels(), color='#000000', fontweight='bold', fontsize=12)
    plt.setp(ax.get_yticklabels(), color='#000000', fontweight='bold', fontsize=12)
    
    # Force axes spines to black
    for spine in ax.spines.values():
        spine.set_edgecolor('#000000')
        spine.set_linewidth(2)
    
    plt.tight_layout()
    
    # Save with ultra settings
    plt.savefig('ULTRA_BLACK_TEXT_TEST.png', 
                dpi=300, 
                facecolor='white',
                edgecolor='#000000',
                bbox_inches='tight',
                pad_inches=0.2)
    
    plt.show()
    
    print("✅ ULTRA BLACK text test saved: ULTRA_BLACK_TEXT_TEST.png")

def create_ultra_kmrl_chart():
    """Create KMRL chart with ULTRA BLACK text"""
    
    ultra_force_black_text()
    
    print("📊 Creating KMRL ULTRA BLACK TEXT chart...")
    
    # Create figure
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
    
    # KMRL data
    models = ['Failure\nPrediction', 'Optimization\nDecision', 'Demand\nForecasting']
    accuracies = [98.6, 100.0, 50.0]
    colors = ['#228B22', '#1E90FF', '#FF4500']  # Darker colors
    
    # Main title with pure black
    fig.suptitle('KMRL ML SYSTEM - ULTRA BLACK TEXT VERSION', 
                 fontsize=20, fontweight='bold', color='#000000')
    
    # Chart 1: Bar chart
    bars = ax1.bar(models, accuracies, color=colors, alpha=0.8, 
                   edgecolor='#000000', linewidth=2)
    
    ax1.set_title('MODEL ACCURACY - PURE BLACK TEXT', 
                  fontsize=16, fontweight='bold', color='#000000')
    ax1.set_ylabel('ACCURACY (%) - BLACK', 
                   fontsize=14, fontweight='bold', color='#000000')
    ax1.set_xlabel('ML MODELS - BLACK', 
                   fontsize=14, fontweight='bold', color='#000000')
    ax1.set_ylim(0, 105)
    ax1.grid(True, alpha=0.3)
    ax1.tick_params(axis='both', colors='#000000', labelsize=12, width=2)
    
    # Add percentage labels
    for bar, acc in zip(bars, accuracies):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{acc:.1f}%', ha='center', va='bottom', 
                fontsize=12, fontweight='bold', color='#000000')
    
    # Force tick labels to pure black
    plt.setp(ax1.get_xticklabels(), color='#000000', fontweight='bold')
    plt.setp(ax1.get_yticklabels(), color='#000000', fontweight='bold')
    
    # Chart 2: Pie chart  
    sizes = [82.9, 17.1]
    labels = ['Production\nReady', 'Needs\nWork']
    colors_pie = ['#32CD32', '#FFA500']
    
    wedges, texts, autotexts = ax2.pie(sizes, labels=labels, colors=colors_pie,
                                      autopct='%1.1f%%', startangle=90)
    
    ax2.set_title('DEPLOYMENT STATUS - PURE BLACK', 
                  fontsize=16, fontweight='bold', color='#000000')
    
    # Force ALL pie chart text to pure black
    for text in texts:
        text.set_color('#000000')
        text.set_fontweight('bold')
        text.set_fontsize(12)
    
    for autotext in autotexts:
        autotext.set_color('#000000')  
        autotext.set_fontweight('bold')
        autotext.set_fontsize(12)
    
    # Force axes to black
    for ax in [ax1, ax2]:
        for spine in ax.spines.values():
            spine.set_edgecolor('#000000')
            spine.set_linewidth(2)
    
    plt.tight_layout()
    
    # Save with maximum black settings
    plt.savefig('ULTRA_KMRL_BLACK_TEXT.png', 
                dpi=300, 
                facecolor='white',
                edgecolor='#000000',
                bbox_inches='tight',
                pad_inches=0.2)
    
    plt.show()
    
    print("✅ ULTRA KMRL black text saved: ULTRA_KMRL_BLACK_TEXT.png")

def main():
    """Main function"""
    
    print("🚨🚨 ULTRA AGGRESSIVE BLACK TEXT FORCING 🚨🚨")
    print("=" * 60)
    print("This version manually sets EVERY text element to #000000")
    print("=" * 60)
    
    create_ultra_black_test()
    print()
    create_ultra_kmrl_chart()
    
    print("\n" + "=" * 60)
    print("✅ ULTRA BLACK TEXT GRAPHS CREATED!")
    print("📁 Files:")
    print("   • ULTRA_BLACK_TEXT_TEST.png")
    print("   • ULTRA_KMRL_BLACK_TEXT.png")
    print("")
    print("🔍 These use pure black #000000 for ALL text")
    print("🔍 If still light, check your image viewer/monitor")
    print("=" * 60)

if __name__ == "__main__":
    main()