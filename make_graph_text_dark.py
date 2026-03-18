#!/usr/bin/env python
"""
TEMPLATE: How to Make ANY Graph Text DARK/BLACK
Simple function to force all text elements to be dark colored
"""

import matplotlib.pyplot as plt
import numpy as np

def force_dark_text():
    """
    🎯 SIMPLE FUNCTION TO MAKE ALL GRAPH TEXT DARK/BLACK
    Call this before creating any plots to ensure dark text
    """
    plt.rcParams.update({
        # ALL TEXT COLORS TO BLACK
        'text.color': 'black',
        'axes.labelcolor': 'black', 
        'axes.titlecolor': 'black',
        'xtick.color': 'black',
        'ytick.color': 'black',
        'legend.edgecolor': 'black',
        
        # BACKGROUND COLORS
        'figure.facecolor': 'white',
        'axes.facecolor': 'white',
        'savefig.facecolor': 'white',
        
        # FONT SETTINGS
        'font.size': 12,
        'font.weight': 'bold'
    })

# EXAMPLE USAGE:
if __name__ == "__main__":
    
    print("🎨 DEMONSTRATION: Making Graph Text DARK")
    print("=" * 45)
    
    # Step 1: Call the function to force dark text
    force_dark_text()
    
    # Step 2: Create any graph - ALL TEXT will be DARK
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, 'b-', linewidth=2, label='Sin Wave')
    plt.title('EXAMPLE: Graph with DARK TEXT', color='black', fontweight='bold')
    plt.xlabel('X Values', color='black', fontweight='bold')
    plt.ylabel('Y Values', color='black', fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tick_params(colors='black')
    
    # Save with dark text
    plt.savefig('example_dark_text.png', dpi=300, facecolor='white', 
                bbox_inches='tight')
    
    print("✅ Example graph created: example_dark_text.png")
    print("✅ ALL TEXT IS DARK/BLACK!")
    print("\n📋 HOW TO USE:")
    print("1. Import this file: from make_graph_text_dark import force_dark_text")
    print("2. Call force_dark_text() before creating plots")
    print("3. Create your graphs normally - text will be dark!")
    print("=" * 45)