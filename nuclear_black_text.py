#!/usr/bin/env python
"""
NUCLEAR APPROACH - FINAL SOLUTION FOR BLACK TEXT
This uses EVERY possible method to force black text
"""

import matplotlib
matplotlib.use('Agg')  # Force non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import warnings
warnings.filterwarnings('ignore')

def nuclear_reset_matplotlib():
    """Nuclear reset of matplotlib to force black text"""
    
    # Complete nuclear reset
    plt.close('all')
    plt.clf()
    plt.cla()
    matplotlib.rcdefaults()
    
    # Set backend explicitly
    matplotlib.use('Agg')
    
    # NUCLEAR parameter override - set EVERYTHING to black
    nuclear_params = {
        # TEXT - PURE BLACK
        'text.color': 'k',  # Use 'k' for black
        'axes.labelcolor': 'k',
        'axes.titlecolor': 'k', 
        'xtick.color': 'k',
        'ytick.color': 'k',
        'legend.edgecolor': 'k',
        'axes.edgecolor': 'k',
        
        # BACKGROUNDS - WHITE  
        'figure.facecolor': 'w',
        'axes.facecolor': 'w',
        'savefig.facecolor': 'w',
        'legend.facecolor': 'w',
        
        # FONT SETTINGS
        'font.family': 'DejaVu Sans',
        'font.size': 16,
        'font.weight': 'bold',
        'axes.titlesize': 20,
        'axes.titleweight': 'bold',
        'axes.labelsize': 18,
        'axes.labelweight': 'bold',
        'xtick.labelsize': 14,
        'ytick.labelsize': 14,
        'legend.fontsize': 14,
        
        # STYLE SETTINGS
        'axes.linewidth': 2,
        'xtick.major.width': 2,
        'ytick.major.width': 2,
        'xtick.minor.width': 1,
        'ytick.minor.width': 1,
        'xtick.major.size': 8,
        'ytick.major.size': 8,
        
        # GRID
        'grid.color': 'gray',
        'grid.alpha': 0.3,
        'grid.linewidth': 1,
    }
    
    # Apply with multiple methods
    plt.rcParams.update(nuclear_params)
    matplotlib.rcParams.update(nuclear_params)
    
    # Also set rcParams directly
    for key, value in nuclear_params.items():
        plt.rcParams[key] = value
        matplotlib.rcParams[key] = value

def create_nuclear_test():
    """Create test with nuclear black text approach"""
    
    nuclear_reset_matplotlib()
    
    print("💣 NUCLEAR BLACK TEXT TEST - Using ALL methods...")
    
    # Create figure with explicit settings
    fig = plt.figure(figsize=(12, 8), facecolor='white')
    ax = fig.add_subplot(111, facecolor='white')
    
    # Test data
    x = ['Model A', 'Model B', 'Model C', 'Model D']
    y = [85, 92, 78, 95]
    colors = ['red', 'blue', 'green', 'orange']
    
    # Create bars with black edges
    bars = ax.bar(x, y, color=colors, alpha=0.7, edgecolor='black', linewidth=3)
    
    # Set title with multiple black specifications
    title = fig.suptitle('NUCLEAR BLACK TEXT TEST', 
                        fontsize=24, 
                        fontweight='bold', 
                        color='black',
                        family='monospace')
    title.set_color('k')  # Force to black again
    
    # Set axis labels with multiple black specifications
    ax.set_title('THIS TEXT MUST BE BLACK', 
                fontsize=20, fontweight='bold', color='black')
    ax.set_xlabel('CATEGORIES', fontsize=18, fontweight='bold', color='black')
    ax.set_ylabel('VALUES', fontsize=18, fontweight='bold', color='black')
    
    # Force all text elements to black manually
    ax.title.set_color('black')
    ax.xaxis.label.set_color('black')
    ax.yaxis.label.set_color('black')
    
    # Set tick parameters
    ax.tick_params(axis='both', colors='black', labelsize=14, width=2, length=6)
    ax.grid(True, alpha=0.3, color='gray')
    
    # Add value labels with explicit black
    for bar, val in zip(bars, y):
        height = bar.get_height()
        text = ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                      f'{val}%', ha='center', va='bottom', 
                      fontsize=16, fontweight='bold', color='black')
        text.set_color('black')  # Force again
    
    # NUCLEAR approach - manually set every tick label
    for label in ax.get_xticklabels():
        label.set_color('black')
        label.set_fontweight('bold')
        label.set_fontsize(14)
    
    for label in ax.get_yticklabels():
        label.set_color('black')
        label.set_fontweight('bold')  
        label.set_fontsize(14)
    
    # Force spine colors
    for spine in ax.spines.values():
        spine.set_edgecolor('black')
        spine.set_linewidth(2)
    
    # Add text box with black text
    textstr = 'ALL TEXT SHOULD BE BLACK'
    props = dict(boxstyle='round', facecolor='white', edgecolor='black', linewidth=2)
    ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=14,
            verticalalignment='top', bbox=props, color='black', fontweight='bold')
    
    plt.tight_layout()
    
    # Save with explicit settings
    plt.savefig('NUCLEAR_BLACK_TEXT.png', 
                dpi=300,
                facecolor='white',
                edgecolor='black',
                bbox_inches='tight',
                pad_inches=0.2)
    
    print("✅ NUCLEAR test saved: NUCLEAR_BLACK_TEXT.png")
    
    plt.close()

def create_simple_black_chart():
    """Create the simplest possible chart with black text"""
    
    nuclear_reset_matplotlib()
    
    print("📊 Creating SIMPLE BLACK TEXT chart...")
    
    # Simplest possible approach
    fig, ax = plt.subplots(figsize=(8, 6), facecolor='white')
    
    # Simple bar chart
    categories = ['A', 'B', 'C']
    values = [30, 60, 90]
    
    bars = ax.bar(categories, values, color=['red', 'green', 'blue'], 
                 edgecolor='black', linewidth=2)
    
    # Set all text to black explicitly
    ax.set_title('SIMPLE BLACK TEXT TEST', color='black', fontsize=18, weight='bold')
    ax.set_xlabel('Items', color='black', fontsize=14, weight='bold')
    ax.set_ylabel('Count', color='black', fontsize=14, weight='bold')
    
    # Force tick colors
    ax.tick_params(colors='black', labelsize=12)
    
    # Manually color every element
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_color('black')
        label.set_weight('bold')
    
    # Add labels on bars
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
               str(val), ha='center', va='bottom', color='black', 
               fontsize=12, weight='bold')
    
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('SIMPLE_BLACK_TEST.png', dpi=300, facecolor='white')
    
    print("✅ SIMPLE test saved: SIMPLE_BLACK_TEST.png")
    
    plt.close()

def create_text_only_test():
    """Create chart that's mostly just text to test visibility"""
    
    nuclear_reset_matplotlib()
    
    print("📝 Creating TEXT-ONLY visibility test...")
    
    fig, ax = plt.subplots(figsize=(10, 8), facecolor='white')
    
    # Remove axes to focus on text
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Add multiple text elements in different sizes
    texts = [
        "LARGE BLACK TEXT - Size 24",
        "Medium Black Text - Size 18", 
        "Normal Black Text - Size 14",
        "Small Black Text - Size 12",
        "BOLD BLACK TEXT",
        "Regular Black Text"
    ]
    
    sizes = [24, 18, 14, 12, 16, 14]
    weights = ['bold', 'normal', 'normal', 'normal', 'bold', 'normal']
    
    for i, (text, size, weight) in enumerate(zip(texts, sizes, weights)):
        y_pos = 9 - i * 1.3
        ax.text(5, y_pos, text, ha='center', va='center',
               fontsize=size, color='black', weight=weight)
    
    # Add border
    rect = patches.Rectangle((0.5, 0.5), 9, 9, linewidth=3, 
                           edgecolor='black', facecolor='none')
    ax.add_patch(rect)
    
    plt.tight_layout()
    plt.savefig('TEXT_VISIBILITY_TEST.png', dpi=300, facecolor='white')
    
    print("✅ TEXT test saved: TEXT_VISIBILITY_TEST.png")
    
    plt.close()

def diagnose_system():
    """Diagnose system settings that might affect text color"""
    
    print("🔍 SYSTEM DIAGNOSIS:")
    print("=" * 40)
    
    # Check matplotlib version and backend
    print(f"Matplotlib version: {matplotlib.__version__}")
    print(f"Current backend: {matplotlib.get_backend()}")
    
    # Check rcParams
    print(f"Text color setting: {plt.rcParams['text.color']}")
    print(f"Axes label color: {plt.rcParams['axes.labelcolor']}")
    print(f"Figure facecolor: {plt.rcParams['figure.facecolor']}")
    
    print("\n🔍 MOST LIKELY ISSUES:")
    print("1. Windows display scaling/DPI settings")
    print("2. Graphics driver color management") 
    print("3. Image viewer gamma/brightness settings")
    print("4. System dark/light mode affecting rendering")
    print("5. Monitor brightness/contrast settings")
    print("6. Windows High Contrast mode")

def main():
    """Main nuclear approach"""
    
    print("💣💣 NUCLEAR BLACK TEXT APPROACH 💣💣")
    print("=" * 50)
    print("Using EVERY possible method to force black text")
    print("=" * 50)
    
    # Run all tests
    create_nuclear_test()
    print()
    create_simple_black_chart()
    print()
    create_text_only_test()
    print()
    diagnose_system()
    
    print("\n" + "=" * 50)
    print("💣 NUCLEAR APPROACH COMPLETE!")
    print("📁 Files created:")
    print("   • NUCLEAR_BLACK_TEXT.png")  
    print("   • SIMPLE_BLACK_TEST.png")
    print("   • TEXT_VISIBILITY_TEST.png")
    print("")
    print("🔍 If STILL light after this:")
    print("   → The issue is NOT in the code")
    print("   → Check Windows display settings")
    print("   → Check your image viewer")  
    print("   → Check monitor brightness/contrast")
    print("=" * 50)

if __name__ == "__main__":
    main()