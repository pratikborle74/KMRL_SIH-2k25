#!/usr/bin/env python
"""
FINAL DIAGNOSTIC - Find the exact cause of light text
This creates test images that will help identify the specific issue
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os

def create_pure_black_bitmap():
    """Create a bitmap with pure black pixels - no matplotlib involved"""
    
    print("🔍 Creating pure black bitmap test (no matplotlib)...")
    
    # Create pure black text on white background using PIL
    width, height = 800, 600
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    try:
        # Try to use a system font
        font = ImageFont.truetype("arial.ttf", 48)
    except:
        font = ImageFont.load_default()
    
    # Draw pure black text
    text_lines = [
        "PURE BLACK TEXT TEST",
        "This is RGB (0,0,0) black",
        "If this appears light/gray,",
        "the issue is your display/viewer"
    ]
    
    y_pos = 100
    for line in text_lines:
        # Draw with pure black (0,0,0)
        draw.text((50, y_pos), line, fill=(0, 0, 0), font=font)
        y_pos += 80
    
    # Add a pure black rectangle
    draw.rectangle([50, 450, 750, 550], fill=(0, 0, 0))
    draw.text((60, 480), "PURE BLACK RECTANGLE - RGB(0,0,0)", fill=(255, 255, 255), font=font)
    
    image.save('PURE_BLACK_BITMAP.png')
    print("✅ Saved: PURE_BLACK_BITMAP.png")
    
    return image

def create_grayscale_test():
    """Create grayscale gradient to test color perception"""
    
    print("🔍 Creating grayscale gradient test...")
    
    width, height = 800, 100
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    # Create gradient from white to black
    for x in range(width):
        gray_value = int(255 * (1 - x / width))
        color = (gray_value, gray_value, gray_value)
        draw.line([(x, 0), (x, height)], fill=color)
    
    # Add labels
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()
    
    # White text on black background
    draw.text((650, 10), "Pure Black", fill=(255, 255, 255), font=font)
    draw.text((50, 10), "Pure White", fill=(0, 0, 0), font=font)
    
    image.save('GRAYSCALE_GRADIENT_TEST.png')
    print("✅ Saved: GRAYSCALE_GRADIENT_TEST.png")

def create_matplotlib_vs_pil_comparison():
    """Compare matplotlib output vs PIL output side by side"""
    
    print("🔍 Creating matplotlib vs PIL comparison...")
    
    # Create matplotlib version
    plt.figure(figsize=(8, 4), facecolor='white')
    plt.text(0.5, 0.5, 'MATPLOTLIB BLACK TEXT', 
             fontsize=24, color='black', weight='bold',
             ha='center', va='center', transform=plt.gca().transAxes)
    plt.axis('off')
    plt.savefig('MATPLOTLIB_BLACK.png', dpi=150, facecolor='white', bbox_inches='tight')
    plt.close()
    
    # Create PIL version  
    image = Image.new('RGB', (600, 300), 'white')
    draw = ImageDraw.Draw(image)
    
    try:
        font = ImageFont.truetype("arial.ttf", 36)
    except:
        font = ImageFont.load_default()
    
    draw.text((300, 150), 'PIL BLACK TEXT', fill=(0, 0, 0), font=font, anchor='mm')
    image.save('PIL_BLACK.png')
    
    print("✅ Saved: MATPLOTLIB_BLACK.png and PIL_BLACK.png")

def analyze_png_file():
    """Analyze the actual RGB values in our PNG files"""
    
    print("🔍 Analyzing actual RGB values in PNG files...")
    
    try:
        # Check if we can read the PNG and examine pixel values
        if os.path.exists('PURE_BLACK_BITMAP.png'):
            image = Image.open('PURE_BLACK_BITMAP.png')
            
            # Sample some pixels
            width, height = image.size
            
            # Check text area pixels
            text_pixel = image.getpixel((100, 100))  # Should be black text
            bg_pixel = image.getpixel((400, 50))     # Should be white background
            rect_pixel = image.getpixel((100, 500))  # Should be black rectangle
            
            print(f"📊 ACTUAL PIXEL VALUES:")
            print(f"   Text pixel RGB: {text_pixel}")
            print(f"   Background pixel RGB: {bg_pixel}")  
            print(f"   Rectangle pixel RGB: {rect_pixel}")
            
            if text_pixel == (0, 0, 0):
                print("✅ Text pixels are PURE BLACK (0,0,0)")
            else:
                print(f"❌ Text pixels are NOT pure black: {text_pixel}")
                
        else:
            print("❌ Could not find test image to analyze")
            
    except Exception as e:
        print(f"❌ Error analyzing PNG: {e}")

def create_system_info_report():
    """Create a system information report"""
    
    print("🔍 Generating system information...")
    
    info = []
    info.append("=== SYSTEM DIAGNOSTIC REPORT ===")
    info.append(f"Python Version: {os.sys.version}")
    info.append(f"Matplotlib Version: {matplotlib.__version__}")
    info.append(f"Matplotlib Backend: {matplotlib.get_backend()}")
    info.append(f"PIL Available: {'Yes' if 'PIL' in globals() else 'No'}")
    
    # Check text color settings
    info.append(f"MPL text.color: {plt.rcParams['text.color']}")
    info.append(f"MPL axes.labelcolor: {plt.rcParams['axes.labelcolor']}")
    info.append(f"MPL figure.facecolor: {plt.rcParams['figure.facecolor']}")
    
    # Windows specific checks
    info.append("\n=== POTENTIAL WINDOWS ISSUES ===")
    info.append("1. Windows Display Scaling (125%, 150%, etc.)")
    info.append("2. Windows Night Light mode")  
    info.append("3. Windows HDR settings")
    info.append("4. Graphics driver color management")
    info.append("5. Monitor brightness/contrast too high")
    info.append("6. Image viewer gamma correction")
    
    report = '\n'.join(info)
    
    with open('SYSTEM_DIAGNOSTIC_REPORT.txt', 'w') as f:
        f.write(report)
    
    print("✅ Saved: SYSTEM_DIAGNOSTIC_REPORT.txt")
    print("\n" + report)

def main():
    """Run all diagnostic tests"""
    
    print("🚨 FINAL DIAGNOSTIC - IDENTIFYING THE EXACT ISSUE")
    print("=" * 60)
    
    # Run all tests
    create_pure_black_bitmap()
    print()
    create_grayscale_test() 
    print()
    create_matplotlib_vs_pil_comparison()
    print()
    analyze_png_file()
    print()
    create_system_info_report()
    
    print("\n" + "=" * 60)
    print("🔍 DIAGNOSTIC COMPLETE!")
    print("\nFiles created:")
    print("• PURE_BLACK_BITMAP.png - Pure black pixels (no matplotlib)")
    print("• GRAYSCALE_GRADIENT_TEST.png - Gradient test")
    print("• MATPLOTLIB_BLACK.png - Matplotlib version")
    print("• PIL_BLACK.png - PIL version")
    print("• SYSTEM_DIAGNOSTIC_REPORT.txt - System info")
    
    print("\n🧪 TEST INSTRUCTIONS:")
    print("1. Open PURE_BLACK_BITMAP.png in Windows Paint")
    print("2. If the text appears LIGHT/GRAY in Paint:")
    print("   → The issue is your display/graphics settings")
    print("3. If it appears BLACK in Paint but light elsewhere:")
    print("   → The issue is your image viewer")
    
    print("\n🎯 NEXT STEPS:")
    print("If PURE_BLACK_BITMAP.png shows light text in Paint,")
    print("the issue is definitely hardware/driver related.")
    print("=" * 60)

if __name__ == "__main__":
    main()